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
| cifs | name \ndomain \nou \nsession_security \nsmb_encryption \nsmb_signing \ntry_ldap_channel_binding \nrestrict_anonymous \nlm_compatibility_level \nldap_referral_enabled \nkdc_encryption \nis_multichannel_enabled \nencrypt_dc_connection \ndefault_site \naes_netlogon_enabled \nprivileges \nadministrators |
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




