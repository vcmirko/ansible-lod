# ontap / snapshot_policy 
Manage NetApp ONTAP Snapshot Policies  
  






## Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [create](#snapshot_policy--create) |  |



## snapshot_policy / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Create Snapshot Policy  | netapp.ontap | na_ontap_snapshot_policy |  | snapshot_policy, svm |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| snapshot_policy | name<br>schedule<br>snapmirror_label<br>prefix<br>count<br>enabled |
| svm | name |




