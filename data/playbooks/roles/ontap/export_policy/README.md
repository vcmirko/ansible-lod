# ontap / export_policy 
Manage NetApp ONTAP Export Policies and rules  
  






## Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [create](#export_policy--create) |  |
| [delete](#export_policy--delete) |  |



## export_policy / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Create Export Policy | netapp.ontap | na_ontap_export_policy |  | export_policy, svm |
| Create/Delete/Modify export rules | netapp.ontap | na_ontap_export_policy_rule | x | export_policy, svm |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| export_policy | name<br>rules |
| svm | name |



## export_policy / delete

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Delete Export Policy | netapp.ontap | na_ontap_export_policy |  | export_policy, svm |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| export_policy | name |
| svm | name |




