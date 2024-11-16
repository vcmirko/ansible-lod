$keyboard = Read-Host "What keyboard layout do you want ? ex. nl-BE" 
Write-Host "Setting keyboard to Belgian" -ForegroundColor Magenta
powershell -command "Set-WinUserLanguageList -Force '$keyboard'"
Write-Host "Keyboard set!"

$dummy = Read-Host "..."

Write-Host "Creating bookmark for Ansible Forms" -ForegroundColor Magenta
# Define the path to your Chrome bookmarks file
$bookmarksFilePath = "C:\Users\Administrator.DEMO\AppData\Local\Google\Chrome\User Data\Default\Bookmarks"

# Read the JSON data from the file
$jsonData = Get-Content $bookmarksFilePath | ConvertFrom-Json

# Define the new bookmark entry
$newBookmark = @{
    "date_added" = (Get-Date).Ticks
    "guid" = [System.Guid]::NewGuid().ToString()
    "id" = [System.Guid]::NewGuid().ToString()
    "name" = "Ansible Forms"
    "type" = "url"
    "url" = "https://rhel1.demo.netapp.com/#/"
}

# Add the new bookmark to the "bookmark_bar" children
$jsonData.roots.bookmark_bar.children += $newBookmark

# Convert the updated JSON data back to a string
$updatedData = $jsonData | ConvertTo-Json -Depth 5

# Write the updated data back to the bookmarks file
$updatedData | Set-Content $bookmarksFilePath

Write-Host "Bookmark added successfully."


$dummy = Read-Host "... install Ansible Forms now ..."
Write-Host "Creating loopback credentials for self-automation"
add-type @"
    using System.Net;
    using System.Security.Cryptography.X509Certificates;
    public class TrustAllCertsPolicy : ICertificatePolicy {
        public bool CheckValidationResult(
            ServicePoint srvPoint, X509Certificate certificate,
            WebRequest request, int certificateProblem) {
            return true;
        }
    }
"@
[System.Net.ServicePointManager]::CertificatePolicy = New-Object TrustAllCertsPolicy
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Ssl3, [Net.SecurityProtocolType]::Tls, [Net.SecurityProtocolType]::Tls11, [Net.SecurityProtocolType]::Tls12


# Define the login API URL
$loginApiUrl = "https://rhel1.demo.netapp.com/api/v1/auth/login"

# Define your basic authentication credentials
$basicAuth = "YWRtaW46QW5zaWJsZUZvcm1zITEyMw=="

write-host "Getting token"
# Make the HTTP POST request to obtain the access token
$loginResponse = Invoke-RestMethod -Uri $loginApiUrl -Method Post -Headers @{
    "Authorization" = "Basic $basicAuth"
} -ContentType "application/json"


# Check if the login was successful and obtain the access token
if ($loginResponse.token) {
    $accessToken = $loginResponse.token

    write-host "token acquired"
    # Define the API URL for creating a new user
    $apiUrl = "https://rhel1.demo.netapp.com/api/v1/user/"

    # Define the user data
    $userData = @{
        "username" = "loopback"
        "password" = "Netapp12!"
        "group_id" = 1
    }

    # Convert the user data to JSON
    $userDataJson = $userData | ConvertTo-Json

    write-host "Creating loopback user"
    # Make the HTTP POST request to create the user using the access token
    $response = Invoke-RestMethod -Uri $apiUrl -Method Post -Headers @{
        "Authorization" = "Bearer $accessToken"
    } -ContentType "application/json" -Body $userDataJson

    # Check the response
    if ($response) {
        Write-Host "User created successfully."
    } else {
        Write-Host "Failed to create the user."
    }

    write-host "Adding loopback credentials"
    # Define the API URL for creating a new credential
    $apiUrl = "https://rhel1.demo.netapp.com/api/v1/credential/"

    # Define the credential data
    $credentialData = @{
        "name" = "loopback"
        "user" = "loopback"
        "password" = "Netapp12!"
    }

    # Convert the credential data to JSON
    $credentialDataJson = $credentialData | ConvertTo-Json

    # Make the HTTP POST request to create the credential using the access token
    $response = Invoke-RestMethod -Uri $apiUrl -Method Post -Headers @{
        "Authorization" = "Bearer $accessToken"
    } -ContentType "application/json" -Body $credentialDataJson

    # Check the response
    if ($response) {
        Write-Host "Credential created successfully."
    } else {
        Write-Host "Failed to create the credential."
    }

} else {
    Write-Host "Login failed. Unable to obtain an access token."
}

$dummy = Read-Host "Press any key to continue"