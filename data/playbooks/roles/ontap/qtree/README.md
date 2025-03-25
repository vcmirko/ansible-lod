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
| qtree | name \nexport_policy \nsecurity_style \nunix_permissions \nunix_group \nunix_user \nwait_for_completion |
| svm | name |
| volume | name |




