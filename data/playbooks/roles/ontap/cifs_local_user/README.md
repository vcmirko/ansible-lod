# ontap / cifs_local_user

This role is used to create a cifs local user on an svm.

## tasks

- create : create a cifs local user on an svm (required credentials : ontap)

## Input

- cluster.management_ip
- svm.name
- cifs_local_user.name
- cifs_local_user.password
- cifs_local_user.full_name
- cifs_local_user.account_disabled
- cifs_local_user.description
- cifs_local_group.name

## execution

**create** :

- na_ontap_cifs_local_user