# Playbooks

| Playbook |
| :--- |
| [ansibleforms_alter_user_caching_sha2_password.yaml](#ansibleforms_alter_user_caching_sha2_passwordyaml) |
| [ansibleforms_ansible_galaxy_install.yaml](#ansibleforms_ansible_galaxy_installyaml) |
| [ansibleforms_backup.yaml](#ansibleforms_backupyaml) |
| [ansibleforms_job_cleanup.yaml](#ansibleforms_job_cleanupyaml) |
| [ansibleforms_pip_install.yaml](#ansibleforms_pip_installyaml) |
| [dummy.yaml](#dummyyaml) |
| [lod_init_af.yaml](#lod_init_afyaml) |
| [ontap_test.yaml](#ontap_testyaml) |



## ansibleforms_alter_user_caching_sha2_password.yaml
**Description**:  

No description yet

**Version history**:  

No version history yet


### Alter user for caching sha2 password 

| Option | Value |
| :----- | :---- |
| hosts | localhost |
| gather_facts | False |
| become | False |

**Vars files**:



  
**Roles**:  

| Role | QTask | QChild | Prefix |
| :--- | :---- | :----- | :----- |




## ansibleforms_ansible_galaxy_install.yaml
**Description**:  

No description yet

**Version history**:  

No version history yet


### Ansible-Galaxy Install 

| Option | Value |
| :----- | :---- |
| hosts | localhost |
| gather_facts | False |
| become | False |

**Vars files**:



  
**Roles**:  

| Role | QTask | QChild | Prefix |
| :--- | :---- | :----- | :----- |




## ansibleforms_backup.yaml
**Description**:  

No description yet

**Version history**:  

No version history yet


### backup ansibleforms 

| Option | Value |
| :----- | :---- |
| hosts | localhost |
| gather_facts | False |
| become | True |

**Vars files**:



  
**Roles**:  

| Role | QTask | QChild | Prefix |
| :--- | :---- | :----- | :----- |




## ansibleforms_job_cleanup.yaml
**Description**:  

No description yet

**Version history**:  

No version history yet


### cleanup ansibleforms jobs 

| Option | Value |
| :----- | :---- |
| hosts | localhost |
| gather_facts | False |
| become | False |

**Vars files**:



| Variable | Value |
| :------- | :---- |
| login | {'login_host': '{{ mysql_credential.host}}', 'login_port': '{{ mysql_credential.port}}', 'login_user': '{{ mysql_credential.user }}', 'login_password': '{{ mysql_credential.password }}'} |


  
**Roles**:  

| Role | QTask | QChild | Prefix |
| :--- | :---- | :----- | :----- |




## ansibleforms_pip_install.yaml
**Description**:  

No description yet

**Version history**:  

No version history yet


### Donwload and Install custom Python Library 

| Option | Value |
| :----- | :---- |
| hosts | localhost |
| gather_facts | False |
| become | False |

**Vars files**:



  
**Roles**:  

| Role | QTask | QChild | Prefix |
| :--- | :---- | :----- | :----- |




## dummy.yaml
**Description**:  

No description yet

**Version history**:  

No version history yet


### This is a hello-world example 

| Option | Value |
| :----- | :---- |
| hosts | localhost |
| gather_facts | False |
| become | False |

**Vars files**:



  
**Roles**:  

| Role | QTask | QChild | Prefix |
| :--- | :---- | :----- | :----- |




## lod_init_af.yaml
**Description**:  

No description yet

**Version history**:  

No version history yet


### Perform AF tasks 

| Option | Value |
| :----- | :---- |
| hosts | localhost |
| gather_facts | False |
| become | False |

**Vars files**:



  
**Roles**:  

| Role | QTask | QChild | Prefix |
| :--- | :---- | :----- | :----- |




## ontap_test.yaml
**Description**:  

No description yet

**Version history**:  

No version history yet


### Gather facts 

| Option | Value |
| :----- | :---- |
| hosts | localhost |
| gather_facts | False |
| become | False |

**Vars files**:



| Variable | Value |
| :------- | :---- |
| login | {'username': '{{ netapp_username }}', 'password': '{{ netapp_password }}', 'hostname': '{{ cluster }}', 'https': True, 'validate_certs': False} |


  
**Roles**:  

| Role | QTask | QChild | Prefix |
| :--- | :---- | :----- | :----- |



