# ontap / lif 
Manage NetApp ONTAP Logical Interfaces (LIFs)  
  






## Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [create](#lif--create) |  |
| [delete](#lif--delete) |  |
| [migrate](#lif--migrate) |  |



## lif / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| create lif  | netapp.ontap | na_ontap_interface |  | ipspace, lif, svm |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| ipspace | name |
| lif | address \nname \ninterface_type \nnode \nport \nsubnet_name \nis_auto_revert \nis_dns_update_enabled \nnetmask \nservice_policy |
| svm | name |



## lif / delete

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| delete lif  | netapp.ontap | na_ontap_interface |  | lif, svm |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| lif | name |
| svm | name |



## lif / migrate

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| migrate lif  | netapp.ontap | na_ontap_interface |  | lif, svm |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| lif | name \nnode \nport |
| svm | name |




