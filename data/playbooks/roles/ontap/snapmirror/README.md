# ontap / snapmirror 
Manage NetApp ONTAP Snapmirrors  
  
Note : This role supports multi / looping





## Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [create](#snapmirror--create) |  |
| [delete](#snapmirror--delete) |  |
| [set_retention](#snapmirror--set_retention) |  |
| [update](#snapmirror--update) |  |
| [wait_for_condition](#snapmirror--wait_for_condition) |  |



## snapmirror / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Create Snapmirror  | netapp.ontap | na_ontap_snapmirror |  | snapmirror |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| snapmirror | schedule \npolicy \nidentity_preservation \nmax_transfer_rate |



## snapmirror / delete

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Modify policy SnapMirror (bug fix) - to allow snapmirror break | netapp.ontap | na_ontap_snapmirror |  |  |
| Removing snapmirror  | netapp.ontap | na_ontap_snapmirror |  |  |


**Variables**

| Variable | Properties |
| :------- | :--------- |



## snapmirror / set_retention

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Get snapshot info | netapp.ontap | na_ontap_rest_info |  |  |
| Extract oldest create_date |  | set_fact |  |  |
| diff date |  | set_fact |  |  |
| Calculate keep_days |  | set_fact |  |  |
| Calculate expiration_date |  | set_fact |  |  |
| Changing comment with expiration date | netapp.ontap | na_ontap_volume |  | expiration_date, snapmirror |
| Renaming volume  | netapp.ontap | na_ontap_volume |  | snapmirror |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| expiration_date |  |
| snapmirror | destination |



## snapmirror / update

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Update Snapmirror  | netapp.ontap | na_ontap_snapmirror |  |  |


**Variables**

| Variable | Properties |
| :------- | :--------- |



## snapmirror / wait_for_condition

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Sleep for 10 seconds |  | pause |  |  |
| Wait for Snapmirror  | netapp.ontap | na_ontap_wait_for_condition |  | auth_rest_validate_certs |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| auth_rest_validate_certs |  |




