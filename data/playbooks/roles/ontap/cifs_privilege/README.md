# ontap / cifs_privilege

This role is used to create a cifs privilege on an svm.

## tasks

- create : create a cifs privilege on an svm (required credentials : ontap)

## Input

- cluster.management_ip
- svm.name
- cifs_privilege.name
- cifs_privilege.privileges

## execution

**create** :

- rest call to : protocols/cifs/users-and-groups/privileges

