# ontap / cifs_share_acl 
Manage NetApp ONTAP CIFS share ACLs  
  
Note : This role supports multi / looping





## Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [create](#cifs_share_acl--create) |  |



## cifs_share_acl / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| {{ task_action}} Cifs Share ACL  | netapp.ontap | na_ontap_cifs_acl |  | cifs_share_acl, svm |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| cifs_share_acl | state<br>share_name<br>user_or_group<br>permission<br>type |
| svm | name |




