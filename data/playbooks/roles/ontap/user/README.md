# ontap / user 
Manage NetApp ONTAP Users  
  






## Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [create](#user--create) |  |



## user / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Create user  | netapp.ontap | na_ontap_user |  | svm, user |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| svm | name |
| user | name<br>role_name<br>authentication_password<br>application_strs<br>authentication_method |




