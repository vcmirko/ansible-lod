#!/bin/bash

# Install required tools
echo "--------------------------------------"
echo "Installing required tools..."
echo ""
dnf install -y vim podman-compose jq
echo "--------------------------------------"

# Set permissions for the data folder
echo ""
echo "--------------------------------------"
echo "Setting permissions for the data folder..."
echo ""
chmod -R 664 ./data
chmod -R +x ./data/mysql/init/
echo "--------------------------------------"

# Start the containers
echo ""
echo "--------------------------------------"
echo "Starting containers..."
echo ""
podman-compose up -d
podman-compose ps
echo "--------------------------------------"

echo ""
echo ""
echo ""
echo "--------------------------------------"
echo "Preparing Hashicorp Vault..."
echo ""

VAULT_CONTAINER="af_vault"
AF_CONTAINER="af_app"
VAULT_ADDR="http://rhel1.demo.netapp.com:8200"

echo "Waiting for Vault to start..."
until curl -s $VAULT_ADDR/v1/sys/health | grep -q '"initialized":false'; do
    sleep 2
done

echo "Initializing Vault..."
INIT_OUTPUT=$(podman exec -it $VAULT_CONTAINER vault operator init -format=json)

# Extract unseal keys and root token
UNSEAL_KEYS=$(echo $INIT_OUTPUT | jq -r '.unseal_keys_b64[]')
ROOT_TOKEN=$(echo $INIT_OUTPUT | jq -r '.root_token')

# set the unseal keys 1, 2, 3
UNSEAL_KEY1=$(echo $UNSEAL_KEYS | awk '{print $1}')
UNSEAL_KEY2=$(echo $UNSEAL_KEYS | awk '{print $2}')
UNSEAL_KEY3=$(echo $UNSEAL_KEYS | awk '{print $3}')

# create an unseal script with the unseal keys hardcoded
# and cron schedule to run it every 1 hour with a check if vault is sealed
echo "Creating unseal script you can use later..."
cat <<EOF > /srv/apps/ansible-lod/unseal.sh
#!/bin/bash

VAULT_CONTAINER="af_vault"

if [ "\$(podman exec \$VAULT_CONTAINER vault status -format=json | jq -r '.sealed')" == "true" ]; then
    echo "Vault is sealed. Unsealing..."
    podman exec -it \$VAULT_CONTAINER vault operator unseal $UNSEAL_KEY1
    podman exec -it \$VAULT_CONTAINER vault operator unseal $UNSEAL_KEY2
    podman exec -it \$VAULT_CONTAINER vault operator unseal $UNSEAL_KEY3
else
    echo "Vault is unsealed."
fi

EOF

# Make the script executable
chmod +x /srv/apps/ansible-lod/unseal.sh   

# Create a cron job to run the script every hour
echo "Creating cron job to unseal every 1 hour..."
(crontab -l 2>/dev/null; echo "0 * * * * /srv/apps/ansible-lod/unseal.sh") | crontab -
echo "Cron job created."

# Replace <VAULT_TOKEN> placeholder in .env file
echo "Preparing ansible forms to work with Vault..."
if [ -f .env ]; then
    sed -i "s/<VAULT_TOKEN>/$ROOT_TOKEN/" .env
    echo "Replaced <VAULT_TOKEN> in .env file."
else
    echo ".env file not found. Skipping token replacement."
fi

echo ""
echo "----------------------------"
echo "Vault setup complete."
echo "----------------------------"
echo ""


# Restart the containers to apply the changes
echo ""
echo "----------------------------"
echo "Restarting containers to apply changes..."
echo ""
podman-compose down
podman-compose up -d

echo ""
echo "Containers restarted."
echo "----------------------------"
echo ""
echo ""
echo "Unsealing vault..."
echo "----------------------------"
. unseal.sh

echo ""
echo ""
echo "----------------------------"
echo "Logging in with root token to test..."
podman exec -it $VAULT_CONTAINER vault login $ROOT_TOKEN
echo "----------------------------"
echo ""

# Enable the secrets engine "ansibleforms"
echo ""
echo "----------------------------"
echo "Enabling secrets engine 'ansibleforms'..."
DUMMY=$(curl --header "X-Vault-Token: $ROOT_TOKEN" \
     --request POST \
     --data '{"path":"ansibleforms","type":"kv","config":{"max_lease_ttl":0,"listing_visibility":"hidden","id":"ansibleforms"},"options":{"version":2},"id":"ansibleforms"}' \
     $VAULT_ADDR/v1/sys/mounts/ansibleforms)

# Add the secret "ontap" to the "ansibleforms" secrets engine
echo "Adding secret 'ontap' to 'ansibleforms'..."
DUMMY=$(curl --header "X-Vault-Token: $ROOT_TOKEN" \
     --request POST \
     --data '{"data":{"user":"admin","password":"Netapp1!"},"options":{"cas":0}}' \
     $VAULT_ADDR/v1/ansibleforms/data/ontap)

echo "Secret 'ontap' added to 'ansibleforms'."
echo "----------------------------"
echo ""

# Add the secret "ontap" to the "ansibleforms" secrets engine
echo "Adding secret 'ad' to 'ansibleforms'..."
DUMMY=$(curl --header "X-Vault-Token: $ROOT_TOKEN" \
     --request POST \
     --data '{"data":{"user":"administrator","password":"Netapp1!"},"options":{"cas":0}}' \
     $VAULT_ADDR/v1/ansibleforms/data/ad)

echo "Secret 'ad' added to 'ansibleforms'."
echo "----------------------------"
echo ""

echo ""
echo "----------------------------"
echo "Preparing AnsibleForms..."
echo ""
# Define the login API URL
LOGIN_API_URL="https://rhel1.demo.netapp.com/api/v1/auth/login"
BASIC_AUTH="YWRtaW46TmV0YXBwMSE="

# Loop until the token is acquired
while true; do
    echo "Getting token..."
    LOGIN_RESPONSE=$(curl -s -k -X POST -H "Authorization: Basic $BASIC_AUTH" -H "Content-Type: application/json" $LOGIN_API_URL)
    ACCESS_TOKEN=$(echo $LOGIN_RESPONSE | jq -r '.token')

    if [ "$ACCESS_TOKEN" != "" ]; then
        # echo "Token acquired: $ACCESS_TOKEN"
        break
    else
        echo "AnsibleForms not running yet. Retrying in 5 seconds..."
        sleep 5
    fi
done

# Create a loopback user
USER_API_URL="https://rhel1.demo.netapp.com/api/v1/user/"
USER_DATA=$(jq -n --arg username "loopback" --arg password "Netapp1!" --arg email "" --argjson group_id 1 '{
    username: $username,
    password: $password,
    email: $email,
    group_id: $group_id
}')

echo "Creating loopback user..."
DUMMY=$(curl -s -k -X POST -H "Authorization: Bearer $ACCESS_TOKEN" -H "Content-Type: application/json" -d "$USER_DATA" $USER_API_URL)

# Create loopback credentials
CREDENTIAL_API_URL="https://rhel1.demo.netapp.com/api/v1/credential/"
CREDENTIAL_DATA=$(jq -n --arg name "loopback" --arg user "loopback" --arg host "localhost" --arg description "Loopback credential for self-automation" --arg password "Netapp1!" --argjson port 443 '{
    name: $name,
    user: $user,
    port: $port,
    host: $host,
    description: $description,
    password: $password
}')

echo "Creating loopback credentials..."
DUMMY=$(curl -s -k -X POST -H "Authorization: Bearer $ACCESS_TOKEN" -H "Content-Type: application/json" -d "$CREDENTIAL_DATA" $CREDENTIAL_API_URL)

# Create local database credentials
CREDENTIAL_API_URL="https://rhel1.demo.netapp.com/api/v1/credential/"
CREDENTIAL_DATA=$(jq -n --arg name "self" --arg user "root" --arg host "rhel1.demo.netapp.com" --arg description "" --arg password "AnsibleForms!123" --argjson port 3306 --argjson secure 1 --arg db_type "mysql" --arg db_name "" '{
    name: $name,
    user: $user,
    port: $port,
    host: $host,
    description: $description,
    password: $password,
    secure: $secure,
    db_type: $db_type,
    db_name: $db_name,
    is_database: 1
}')
echo "Creating local database credentials..."
DUMMY=$(curl -s -k -X POST -H "Authorization: Bearer $ACCESS_TOKEN" -H "Content-Type: application/json" -d "$CREDENTIAL_DATA" $CREDENTIAL_API_URL)


# Update settings
SETTINGS_API_URL="https://rhel1.demo.netapp.com/api/v1/settings/"
SETTINGS_DATA=$(jq -n --arg mail_server "rhel1.demo.netapp.com" --argjson mail_port 25 --argjson mail_secure 0 --arg mail_username "" --arg mail_password "" --arg mail_from "rhel1@demo.netapp.com" --arg url "https://rhel1.demo.netapp.com" --arg forms_yaml "" --argjson enableFormsYamlInDatabase false '{
    mail_server: $mail_server,
    mail_port: $mail_port,
    mail_secure: $mail_secure,
    mail_username: $mail_username,
    mail_password: $mail_password,
    mail_from: $mail_from,
    url: $url,
    forms_yaml: $forms_yaml,
    enableFormsYamlInDatabase: $enableFormsYamlInDatabase
}')

echo "Updating settings..."
DUMMY=$(curl -s -k -X PUT -H "Authorization: Bearer $ACCESS_TOKEN" -H "Content-Type: application/json" -d "$SETTINGS_DATA" $SETTINGS_API_URL)

echo "Adding data schemas..."
SCHEMA_API_URL="https://rhel1.demo.netapp.com/api/v1/datasource/schema/"
SCHEMA_DATA=$(jq -n --arg name "lod_env" \
    --arg description "Lab on demand environment" \
    --arg table_definitions "$(printf 'location:\n  - {name: name, unique: true}\n  - {name: code, length: 3, unique: true}\nenvironment:\n  - {name: name, unique: true}\n  - {name: code, length: 3, unique: true}\nservice_level:\n  - {name: name, unique: true}\n  - {name: code, length: 1, unique: true}\nservice:\n  - {name: name, unique: true}\n  - {name: code, length: 3, unique: true}\n  - {name: protocol, length: 5}\nresource:\n  - {name: location, foreign_key: location}\n  - {name: environment, foreign_key: environment}\n  - {name: service_level, foreign_key: service_level}\n  - {name: service, foreign_key: service}\n  - {name: cluster, length: 20}\n  - {name: dr, length: 20}\n  - {name: code, unique:true}')" \
    '{
        name: $name,
        description: $description,
        table_definitions: $table_definitions
    }')

schema_id=$(curl -s -k -X POST -H "Authorization: Bearer $ACCESS_TOKEN" -H "Content-Type: application/json" -d "$SCHEMA_DATA" $SCHEMA_API_URL | jq -r '.data.output')

echo "Resetting schema..."
SCHEMA_RESET_API_URL="https://rhel1.demo.netapp.com/api/v1/datasource/schema/$schema_id/reset/"
DUMMY=$(curl -s -k -X POST -H "Authorization: Bearer $ACCESS_TOKEN" -H "Content-Type: application/json" $SCHEMA_RESET_API_URL)

echo "Adding datasource..."
DATASOURCE_API_URL="https://rhel1.demo.netapp.com/api/v1/datasource/"
DATASOURCE_DATA=$(jq -n --arg name "lod_env" --arg schema "lod_env" --arg form "Datasource lod env" --arg extra_vars "$(printf 'excel_path: ./datasources/excel_files/lod_env.xlsx\nimport_path: ./datasources\naf_datasource_import_hash_ids: true\naf_datasource_import_keep: true')" '{
    name: $name,
    schema: $schema,
    form: $form,
    extra_vars: $extra_vars
}')

datasource_id=$(curl -s -k -X POST -H "Authorization: Bearer $ACCESS_TOKEN" -H "Content-Type: application/json" -d "$DATASOURCE_DATA" $DATASOURCE_API_URL | jq -r '.data.output')

echo "Importing datasource..."
DUMMY=$(curl -s -k -X POST -H "Authorization: Bearer $ACCESS_TOKEN" -H "Content-Type: application/json" -d "{}" "https://rhel1.demo.netapp.com/api/v1/datasource/$datasource_id/import/")

alias "docker=podman"
alias "docker-compose=podman-compose"

# create some space and print the keys and token between 2 lines so it can picked up easily

echo ""
echo ""
echo "--------------------------------------"
echo "Unseal keys:"
echo ""
# echo $UNSEAL_KEYS but as separate lines
echo $UNSEAL_KEYS | tr ' ' '\n'
echo "--------------------------------------"
echo "Root token:"
echo ""
echo $ROOT_TOKEN
echo "--------------------------------------"
echo ""
echo ""
echo "" Write thos the above keys and token to manage the Hasicorp Vault
echo "" You can run the unseal.sh script to unseal the vault
echo ""
echo "Setup complete. You can now access AnsibleForms."
echo "----------------------------"