
$keyboardLayouts = @("nl-BE", "en-US", "de-DE")
for($i = 0; $i -lt $keyboardLayouts.Length; $i++) {
    Write-Host "$($i + 1). $($keyboardLayouts[$i])"
}
do{
    $keyboard = Read-Host "What keyboard layout do you want ? " # 
    $keyboardLayout = $keyboardLayouts[$keyboard - 1]
} while($keyboard -eq "" -or $keyboard -lt 1 -or $keyboard -gt $keyboardLayouts.Length)
Write-Host "Setting keyboard to $keyboardLayout" -ForegroundColor Magenta
powershell -command "Set-WinUserLanguageList -Force '$keyboardLayout'"
Write-Host "Keyboard set!"

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

$newBookmark2 = @{
    "date_added" = (Get-Date).Ticks
    "guid" = [System.Guid]::NewGuid().ToString()
    "id" = [System.Guid]::NewGuid().ToString()
    "name" = "Mail Server"
    "type" = "url"
    "url" = "http://rhel1.demo.netapp.com:1080"
}

$newBookmark3 = @{
    "date_added" = (Get-Date).Ticks
    "guid" = [System.Guid]::NewGuid().ToString()
    "id" = [System.Guid]::NewGuid().ToString()
    "name" = "HashiCorp Vault"
    "type" = "url"
    "url" = "http://rhel1.demo.netapp.com:8200"
}

# Add the new bookmark to the "bookmark_bar" children
$jsonData.roots.bookmark_bar.children += $newBookmark
$jsonData.roots.bookmark_bar.children += $newBookmark2
$jsonData.roots.bookmark_bar.children += $newBookmark3

# Convert the updated JSON data back to a string
$updatedData = $jsonData | ConvertTo-Json -Depth 5

# Write the updated data back to the bookmarks file
$updatedData | Set-Content $bookmarksFilePath

Write-Host "Bookmarks added successfully."

$explanationToShow = @"

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


ssh to the redhat server, and execute the following commands:
Use putty to connect to rhel1.demo.netapp.com

username: root
password: Netapp1!


>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Disable SELinux
sudo setenforce 0

# Install git
dnf install -y git

# Create the apps folder
mkdir -p /srv/apps
cd /srv/apps

# Clone the ansible-lod repository
git clone https://github.com/vcmirko/ansible-lod.git
cd ansible-lod

# run the setup shell script
chmod +x setup.sh
. setup.sh

"@

Write-Host $explanationToShow -ForegroundColor Yellow

$dummy = Read-Host "... Prep the lab on demand with the above command on the rhel1 host, press enter when your are done ..."
$dummy = Read-Host "Open chrome browser and use the bookmark created called 'Ansible Forms' to access the application`r`nContinue the setup from AnsibleForms, see readme from github repository`r`nYou can close this window"

