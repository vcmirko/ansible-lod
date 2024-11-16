# ontap / cifs_share

This role is used to create a cifs share on an svm.

## tasks

- create : create a cifs share on an svm (required credentials : ontap)

## Input

- cluster.management_ip
- svm.name
- cifs_share.path
- cifs_share.name
- cifs_share.comment
- cifs_share.access_based_enumeration
- cifs_share.show_snapshot
- cifs_share.show_previous_versions
- cifs_share.oplocks
- cifs_share.home_directory
- cifs_share.change_notify
- cifs_share.encryption
- cifs_share.namespace_caching
- cifs_share.continuously_available
- cifs_share.browsable
- cifs_share.allow_unencrypted_access
- cifs_share.unix_symlink
- cifs_share.file_security_permissions
- cifs_share.file_security_permissions_acls
- cifs_share.acls

## execution

**create** :

While creating a cifs share, we allow to also add multiple share permissions and ntfs permissions.  

- na_ontap_cifs
- na_ontap_cifs_acl
- na_ontap_file_security_permissions
- na_ontap_file_security_permissions_acl
