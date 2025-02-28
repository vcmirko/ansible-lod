# ontap / qtree 
Manage NetApp ONTAP Qtrees  
  
Note : This role supports multi / looping





## Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [create](#qtree--create) |  |



## qtree / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| create qtree  | netapp.ontap | na_ontap_qtree |  | qtree, svm, volume |
| Set qtree oplocks  | netapp.ontap | na_ontap_rest_cli |  |  |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| qtree | name, <br/>export_policy, <br/>security_style, <br/>unix_permissions, <br/>unix_group, <br/>unix_user, <br/>wait_for_completion |
| svm | name |
| volume | name |




