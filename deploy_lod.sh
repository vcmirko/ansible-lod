set enforce 0

dnf install -y git vim podman-compose

mkdir /srv/apps
cd /srv/apps

git init
git clone https://github.com/ansibleguy76/ansibleforms-docker.git
cd ansibleforms-docker/data/playbooks
wget https://123websites.be/maf.tar 
tar -xf maf.tar
rm -f maf.tar

cd ../../

# write access will be needed on the datafolder
chmod -R 664 ./data
# the mysql init folder needs execute rights 
chmod -R +x ./data/mysql/init/

podman-compose up -d

