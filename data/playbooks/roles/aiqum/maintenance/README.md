# aiqum / maintenance 
Start, stop AIQUM maintenance  
  






## Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [end](#maintenance--end) |  |
| [start](#maintenance--start) |  |



## maintenance / end

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| End maintenance |  | na_aiqum_maintenance |  | aiq_hostname, aiq_password, aiq_username, cluster_name |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| aiq_hostname |  |
| aiq_password |  |
| aiq_username |  |
| cluster_name |  |



## maintenance / start

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Start maintenance |  | na_aiqum_maintenance |  | aiq_hostname, aiq_password, aiq_username, aiqum_ontap_maintenance_hours, cluster_name |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| aiq_hostname |  |
| aiq_password |  |
| aiq_username |  |
| aiqum_ontap_maintenance_hours |  |
| cluster_name |  |




