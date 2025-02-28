# ontap / cifs_share 
Manage NetApp ONTAP CIFS shares  
  
Note : This role supports multi / looping





## Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [create](#cifs_share--create) |  |
| [delete](#cifs_share--delete) |  |



## cifs_share / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Create Cifs Share  | netapp.ontap | na_ontap_cifs |  | cifs_share, svm |
| Get cifs share uuid | netapp.ontap | na_ontap_restit |  |  |
| Set Vscan Profile for Cifs Share  | netapp.ontap | na_ontap_restit |  | cifs_share, cifs_share_info |
| Setting Cifs Share ACLs | netapp.ontap | na_ontap_cifs_acl | x | cifs_share, svm |
| Setting file security permissions for Cifs Share  | netapp.ontap | na_ontap_file_security_permissions |  | cifs_share, svm |
| Setting file security permissions acl for Cifs Share  | netapp.ontap | na_ontap_file_security_permissions_acl | x | cifs_share, svm |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| cifs_share | name, <br/>path, <br/>comment, <br/>access_based_enumeration, <br/>show_snapshot, <br/>show_previous_versions, <br/>oplocks, <br/>home_directory, <br/>change_notify, <br/>encryption, <br/>namespace_caching, <br/>continuously_available, <br/>browsable, <br/>allow_unencrypted_access, <br/>unix_symlink, <br/>acls, <br/>file_security_permissions, <br/>file_security_permissions_acls |
| cifs_share_info | response |
| svm | name |



## cifs_share / delete

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Delete Cifs Share  | netapp.ontap | na_ontap_cifs |  | cifs_share, svm |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| cifs_share | name |
| svm | name |




