set enforce 0

dnf install -y git vim podman-compose

# write access will be needed on the datafolder
chmod -R 664 ./data
# the mysql init folder needs execute rights 
chmod -R +x ./data/mysql/init/

podman-compose up -d

