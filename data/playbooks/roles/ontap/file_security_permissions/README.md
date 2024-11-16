# ontap / file_security_permissions

This role is used to create file security permissions (NTFS) on a cifs share.

## tasks

- create : create file security permissions on a cifs share (required credentials : ontap)

## Input

- cluster.management_ip
- svm.name
- file_security_permissions.access_control
- file_security_permissions.path
- file_security_permissions.owner
- file_security_permissions.acls
- file_security_permissions.propagation_mode
- file_security_permissions.group
