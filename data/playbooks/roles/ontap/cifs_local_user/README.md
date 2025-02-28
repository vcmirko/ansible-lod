# ontap / cifs_local_user 
Manage NetApp ONTAP CIFS local users  
  
Note : This role supports multi / looping





## Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [create](#cifs_local_user--create) |  |



## cifs_local_user / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Create cifs local user  | netapp.ontap | na_ontap_cifs_local_user |  | cifs_local_user, svm |
| Add Cifs Local User  | netapp.ontap | na_ontap_cifs_local_group_member |  | cifs_local_group, cifs_local_user, svm |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| cifs_local_group | name |
| cifs_local_user | name<br>password<br>full_name<br>account_disabled<br>description |
| svm | name |




