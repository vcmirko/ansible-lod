#!/bin/bash

# Install required tools
dnf install -y vim podman-compose jq

# Set permissions for the data folder
chmod -R 664 ./data
chmod -R +x ./data/mysql/init/

# Start the containers
podman-compose up -d

# Show the status
podman-compose ps

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

echo "Unseal Keys:"
echo "$UNSEAL_KEYS"
echo "Root Token: $ROOT_TOKEN"

echo "Unsealing Vault..."
for KEY in $UNSEAL_KEYS; do
    podman exec -it $VAULT_CONTAINER vault operator unseal $KEY
done

echo "Vault unsealed successfully."

# create an unseal script with the unseal keys hardcoded
# and cron schedule to run it every 1 hour with a check if vault is sealed
echo "Creating unseal script..."
cat <<EOF > /srv/apps/ansible-lod/unseal.sh
#!/bin/bash

VAULT_CONTAINER="af_vault"
VAULT_ADDR="http://rhel1.demo.netapp.com:8200"

if [ "\$(podman exec \$VAULT_CONTAINER vault status -format=json | jq -r '.sealed')" == "true" ]; then
    echo "Vault is sealed. Unsealing..."
    podman exec -it \$VAULT_CONTAINER vault operator unseal <UNSEAL_KEY_1>
    podman exec -it \$VAULT_CONTAINER vault operator unseal <UNSEAL_KEY_2>
    podman exec -it \$VAULT_CONTAINER vault operator unseal <UNSEAL_KEY_3>
else
    echo "Vault is unsealed."
fi

EOF

# Replace <UNSEAL_KEY_1>, <UNSEAL_KEY_2>, <UNSEAL_KEY_3> placeholders
sed -i "s/<UNSEAL_KEY_1>/$UNSEAL_KEYS[0]/" /srv/apps/ansible-lod/unseal.sh
sed -i "s/<UNSEAL_KEY_2>/$UNSEAL_KEYS[1]/" /srv/apps/ansible-lod/unseal.sh
sed -i "s/<UNSEAL_KEY_3>/$UNSEAL_KEYS[2]/" /srv/apps/ansible-lod/unseal.sh

# Make the script executable
chmod +x /srv/apps/ansible-lod/unseal.sh    

# Create a cron job to run the script every hour
echo "Creating cron job..."
(crontab -l 2>/dev/null; echo "0 * * * * /srv/apps/ansible-lod/unseal.sh") | crontab -

echo "Cron job created."

echo "Logging in with root token..."
podman exec -it $VAULT_CONTAINER vault login $ROOT_TOKEN

echo "Vault setup complete. Root token: $ROOT_TOKEN"

# Replace <VAULT_TOKEN> placeholder in .env file
if [ -f .env ]; then
    sed -i "s/<VAULT_TOKEN>/$ROOT_TOKEN/" .env
    echo "Replaced <VAULT_TOKEN> in .env file."
else
    echo ".env file not found. Skipping token replacement."
fi

# Restart the containers to apply the changes
podman-compose down
podman-compose up -d

# Enable the secrets engine "ansibleforms"
echo "Enabling secrets engine 'ansibleforms'..."
curl --header "X-Vault-Token: $ROOT_TOKEN" \
     --request POST \
     --data '{"path":"ansibleforms","type":"kv","config":{"max_lease_ttl":0,"listing_visibility":"hidden","id":"ansibleforms"},"options":{"version":2},"id":"ansibleforms"}' \
     $VAULT_ADDR/v1/sys/mounts/ansibleforms

# Add the secret "ontap" to the "ansibleforms" secrets engine
echo "Adding secret 'ontap' to 'ansibleforms'..."
curl --header "X-Vault-Token: $ROOT_TOKEN" \
     --request POST \
     --data '{"data":{"user":"admin","password":"Netapp12"},"options":{"cas":0}}' \
     $VAULT_ADDR/v1/ansibleforms/data/ontap

echo "Secret 'ontap' added to 'ansibleforms'."

# Define the login API URL
LOGIN_API_URL="https://rhel1.demo.netapp.com/api/v1/auth/login"
BASIC_AUTH="YWRtaW46TmV0YXBwMSE="

# Loop until the token is acquired
while true; do
    echo "Getting token..."
    LOGIN_RESPONSE=$(curl -s -k -X POST -H "Authorization: Basic $BASIC_AUTH" -H "Content-Type: application/json" $LOGIN_API_URL)
    ACCESS_TOKEN=$(echo $LOGIN_RESPONSE | jq -r '.token')

    if [ "$ACCESS_TOKEN" != "" ]; then
        echo "Token acquired: $ACCESS_TOKEN"
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
curl -s -k -X POST -H "Authorization: Bearer $ACCESS_TOKEN" -H "Content-Type: application/json" -d "$USER_DATA" $USER_API_URL

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
curl -s -k -X POST -H "Authorization: Bearer $ACCESS_TOKEN" -H "Content-Type: application/json" -d "$CREDENTIAL_DATA" $CREDENTIAL_API_URL

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
curl -s -k -X PUT -H "Authorization: Bearer $ACCESS_TOKEN" -H "Content-Type: application/json" -d "$SETTINGS_DATA" $SETTINGS_API_URL

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
curl -s -k -X POST -H "Authorization: Bearer $ACCESS_TOKEN" -H "Content-Type: application/json" $SCHEMA_RESET_API_URL

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
curl -s -k -X POST -H "Authorization: Bearer $ACCESS_TOKEN" -H "Content-Type: application/json" -d "{}" "https://rhel1.demo.netapp.com/api/v1/datasource/$datasource_id/import/"

echo "Setup complete. You can now access AnsibleForms."

alias "docker=podman"
alias "docker-compose=podman-compose"