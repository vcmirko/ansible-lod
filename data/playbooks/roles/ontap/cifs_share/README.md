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
| cifs_share | name \npath \ncomment \naccess_based_enumeration \nshow_snapshot \nshow_previous_versions \noplocks \nhome_directory \nchange_notify \nencryption \nnamespace_caching \ncontinuously_available \nbrowsable \nallow_unencrypted_access \nunix_symlink \nacls \nfile_security_permissions \nfile_security_permissions_acls |
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




