# ontap / cifs_local_group 
Manage NetApp ONTAP CIFS local groups  
  
Note : This role supports multi / looping





## Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [add](#cifs_local_group--add) |  |
| [create](#cifs_local_group--create) |  |
| [delete](#cifs_local_group--delete) |  |



## cifs_local_group / add

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Add Cifs Local User To Group  | netapp.ontap | na_ontap_cifs_local_group_member | x | cifs_local_group, svm |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| cifs_local_group | name, <br/>members |
| svm | name |



## cifs_local_group / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Create cifs local group  | netapp.ontap | na_ontap_cifs_local_group |  | cifs_local_group, svm |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| cifs_local_group | name |
| svm | name |



## cifs_local_group / delete

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Delete cifs local group  | netapp.ontap | na_ontap_cifs_local_group |  | cifs_local_group, svm |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| cifs_local_group | name |
| svm | name |




