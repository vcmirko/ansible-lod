# ontap / svm 
Manage NetApp ONTAP SVMs (vservers)  
  
Note : This role supports multi / looping





## Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [clean](#svm--clean) |  |
| [create](#svm--create) |  |
| [delete](#svm--delete) |  |



## svm / clean

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Search svm  | netapp.ontap | na_ontap_rest_info |  |  |
| Role - ontap/svm/delete |  | block |  |  |


**Variables**

| Variable | Properties |
| :------- | :--------- |



## svm / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Create Svm  | netapp.ontap | na_ontap_svm |  | ipspace, svm |
| Get aggr list | netapp.ontap | na_ontap_rest_info |  |  |
| Set aggregate list  | netapp.ontap | na_ontap_svm |  | aggr_info, svm |
| Move and rename root volume  | netapp.ontap | na_ontap_volume |  | svm |
| Set SVM Options  | netapp.ontap | na_ontap_svm_options | x | svm |
| Create Lifs  |  | include_tasks | x | svm |
| create default route  | netapp.ontap | na_ontap_net_routes | x | svm |
| Get vserver uuid | netapp.ontap | na_ontap_restit |  |  |
| Set other svm parameters (using restit)  | netapp.ontap | na_ontap_restit |  |  |
| Set other svm parameters (using rest_cli)  | netapp.ontap | na_ontap_rest_cli |  |  |
| Create dns  |  | include_tasks |  |  |
| Enable cifs  |  | include_tasks |  |  |
| Create Domain Tunnel  | netapp.ontap | na_ontap_domain_tunnel |  | svm |
| Set vscan  | netapp.ontap | na_ontap_vscan |  | svm |
| Enable nfs  |  | include_tasks |  |  |
| Enable iscsi  |  | include_tasks |  |  |
| Create volumes on  |  | include_tasks | x | svm |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| aggr_info | ontap_info |
| ipspace | name |
| svm | name<br>allowed_protocols<br>snapshot_policy<br>language<br>comment<br>max_volumes<br>subtype<br>root_volume<br>options<br>lifs<br>vscan_enable<br>volumes |



## svm / delete

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Clean svm  |  | include_tasks |  |  |
| Delete svm  | netapp.ontap | na_ontap_svm |  | svm |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| svm | name |




