# ontap / quota 
Manage NetApp ONTAP Quotas  
  
Note : This role supports multi / looping





## Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [create](#quota--create) |  |
| [delete](#quota--delete) |  |
| [off_on](#quota--off_on) |  |



## quota / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Create/Modify Quota  | netapp.ontap | na_ontap_quotas |  | quota, svm, volume |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| quota | quota_target<br>disk_limit<br>file_limit<br>perform_user_mapping<br>qtree<br>set_quota_status<br>soft_disk_limit<br>soft_file_limit<br>threshold<br>type |
| svm | name |
| volume | name |



## quota / delete

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Delete Quota on  | netapp.ontap | na_ontap_quotas |  | quota, svm, volume |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| quota | quota_target<br>disk_limit<br>file_limit<br>perform_user_mapping<br>qtree<br>set_quota_status<br>soft_disk_limit<br>soft_file_limit<br>threshold<br>type |
| svm | name |
| volume | name |



## quota / off_on

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Set Quota off ->  | netapp.ontap | na_ontap_quotas |  | svm, volume |
| Set Quota on ->  | netapp.ontap | na_ontap_quotas |  | svm, volume |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| svm | name |
| volume | name |




