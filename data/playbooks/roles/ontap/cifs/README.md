# ontap / cifs 
Manage NetApp ONTAP CIFS server  
  






## Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [create](#cifs--create) |  |
| [delete](#cifs--delete) |  |
| [stop](#cifs--stop) |  |



## cifs / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Enable cifs | netapp.ontap | na_ontap_cifs_server |  | ad_password, ad_username, cifs, svm |
| Set cifs options - no rest equivalent | netapp.ontap | na_ontap_rest_cli |  |  |
| Create cifs privileges | netapp.ontap | na_ontap_restit | x | cifs |
| Remove unwanted admins | netapp.ontap | na_ontap_cifs_local_group_member | x | cifs, svm |
| Add extra admins | netapp.ontap | na_ontap_cifs_local_group_member | x | cifs, svm |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| ad_password |  |
| ad_username |  |
| cifs | name, <br/>domain, <br/>ou, <br/>session_security, <br/>smb_encryption, <br/>smb_signing, <br/>try_ldap_channel_binding, <br/>restrict_anonymous, <br/>lm_compatibility_level, <br/>ldap_referral_enabled, <br/>kdc_encryption, <br/>is_multichannel_enabled, <br/>encrypt_dc_connection, <br/>default_site, <br/>aes_netlogon_enabled, <br/>privileges, <br/>administrators |
| svm | name |



## cifs / delete

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Remove cifs | netapp.ontap | na_ontap_cifs_server |  | cifs, svm |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| cifs | name |
| svm | name |



## cifs / stop

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Stop cifs | netapp.ontap | na_ontap_cifs_server |  | cifs, svm |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| cifs | name |
| svm | name |




