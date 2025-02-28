# ontap / snapmirror_policy 
Manage NetApp ONTAP SnapMirror policies  
  






## Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [create](#snapmirror_policy--create) |  |



## snapmirror_policy / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Create Snapmirror Policy  | netapp.ontap | na_ontap_snapmirror_policy |  | snapmirror, svm |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| snapmirror | policy_name, <br/>policy_snapmirror_label, <br/>policy_keep |
| svm | name |




