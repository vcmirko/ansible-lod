# ontap / cifs_local_group

This role is used to create a local group on an svm.

## tasks

- create : create a cifs local group on an svm (required credentials : ontap)
- add : add a user to a cifs local group to an svm (required credentials : ontap)

## Input

- cluster.management_ip
- svm.name
- cifs_local_group.name
- cifs_local_group.members

## execution

**create** :

- na_ontap_cifs_local_group

**add** :

- na_ontap_cifs_local_group_member