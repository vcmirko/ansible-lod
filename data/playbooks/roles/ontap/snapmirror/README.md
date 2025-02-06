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


| Task |
| :--- |
| Create Snapmirror  |



## snapmirror / delete


| Task |
| :--- |
| Modify policy SnapMirror (bug fix) - to allow snapmirror break |
| Removing snapmirror  |



## snapmirror / set_retention


| Task |
| :--- |
| Get snapshot info |
| Extract oldest create_date |
| diff date |
| Calculate keep_days |
| Calculate expiration_date |
| Changing comment with expiration date |
| Renaming volume  |



## snapmirror / update


| Task |
| :--- |
| Update Snapmirror  |



## snapmirror / wait_for_condition


| Task |
| :--- |
| Wait for Snapmirror  |




