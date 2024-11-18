# how to get this running

## Request lod

Use an early adopter lab (tested in ONTAP 9.14.1 v1.2 - Lab ID: RT11196313)

## Initial Jumphost setup (install ansible forms)

Connect to your jump host.

download the following powershell script 
https://github.com/vcmirko/ansible-lod/blob/main/windows_automation.ps1

Run it with powershell on your jumphost.

1. Step 1 : It will allow you to setup the keyboard
2. Step 2 : It will create a bookmark for ansibleforms in the google browser
3. Step 3 : It will wait for manual action

Manual action: Use putty and ssh to rhel1.demo.netapp.com.
Username = root, password = ***standard lod password***
The powershell script will show you the commands, you can run them all at once, that should work.

4. Step 4 : Press enter to continue, the script will wait for AnsibleForms to be deployed
5. Step 5 : A loopback user and credential will be installed in Ansible Forms

## Continue setup in ansible forms

Use chrome, a bookmark should be created called AnsibleForm  

Login with :
user : admin
password : AnsibleForms!123

### Find the 2 forms and run them (under LOD category)

1. Form 1 : Initialize AF for LOD => this will add the ontap and aiqum credentials
2. Form 2 : Setup LOD => this will register the 2 clusters in aiqum and setup ip-ranges in the clusters

# Start experimenting and first tests (under MAF category)

1. Form 1 : Create Svm => allows you to create a basic svm
2. Form 2 : Create Svm DR => allows you to create an svm with svm-dr

... come back, more forms and playbooks will be added.
... in rhel1 under /srv/apps/ansible-lod/ you can run the refresh.sh script, it will refresh new forms and playbook from git
... note that any changes in your forms and playbooks will be lost after a refresh

# Read the README under the data/playbooks/ folder for info about MAF.
