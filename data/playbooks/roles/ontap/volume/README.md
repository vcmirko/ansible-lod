# ontap / volume 
Manage NetApp ONTAP volumes  
  
Note : This role supports multi / looping





## Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [create](#volume--create) |  |
| [create_dp](#volume--create_dp) |  |
| [decom](#volume--decom) |  |
| [delete](#volume--delete) |  |
| [delete_lock](#volume--delete_lock) |  |
| [modify](#volume--modify) |  |
| [move](#volume--move) |  |
| [offline](#volume--offline) |  |
| [online](#volume--online) |  |
| [rename](#volume--rename) |  |
| [resize](#volume--resize) |  |



## volume / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Find best aggregate  |  | get_best_aggregate |  | svm, volume |
| Create volume  | netapp.ontap | na_ontap_volume |  | svm, volume |
| Set efficiency  | netapp.ontap | na_ontap_volume_efficiency |  | svm, volume |
| Set compression type  | netapp.ontap | na_ontap_rest_cli |  |  |
| Set efficiency schedule  | netapp.ontap | na_ontap_rest_cli |  |  |
| Set volume autosize  | netapp.ontap | na_ontap_volume_autosize |  | svm, volume |
| Set volume snapshot autodelete  | netapp.ontap | na_ontap_rest_cli |  |  |
| Set space-mgmt-try-first  | netapp.ontap | na_ontap_rest_cli |  |  |
| Get volume uuid  | netapp.ontap | na_ontap_restit |  |  |
| Set anti-ransomware state  | netapp.ontap | na_ontap_restit |  | volume_info |
| Set read-alloc  | netapp.ontap | na_ontap_rest_cli |  |  |
| Set fractional-reserve  | netapp.ontap | na_ontap_rest_cli |  |  |
| Set atime-update  | netapp.ontap | na_ontap_rest_cli |  |  |
| Create qtrees  |  | include_tasks | x | volume |
| Create luns  |  | include_tasks | x | volume |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| svm | name |
| volume | name, <br/>size, <br/>aggregate_include_node_regex, <br/>activity_tracking, <br/>analytics, <br/>auto_remap_luns, <br/>aggregate, <br/>size_unit, <br/>space_guarantee, <br/>percent_snapshot_space, <br/>wait_for_completion, <br/>junction_path, <br/>language, <br/>comment, <br/>type, <br/>atime_update, <br/>compression, <br/>encrypt, <br/>group_id, <br/>inline_compression, <br/>size_change_threshold, <br/>unix_permissions, <br/>user_id, <br/>security_style, <br/>snaplock, <br/>logical_space_reporting, <br/>logical_space_enforcement, <br/>efficiency_policy, <br/>export_policy, <br/>snapshot_policy, <br/>tiering_policy, <br/>qos_policy_group, <br/>qos_adaptive_policy_group, <br/>volume_efficiency, <br/>volume_autosize, <br/>qtrees, <br/>luns |
| volume_info | response |



## volume / create_dp

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Find best aggregate  |  | get_best_aggregate |  | svm, volume |
| Create dp volume  | netapp.ontap | na_ontap_volume |  | svm, volume |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| svm | name |
| volume | name, <br/>size, <br/>aggregate_include_node_regex, <br/>aggregate, <br/>activity_tracking, <br/>analytics, <br/>size_unit, <br/>space_guarantee, <br/>percent_snapshot_space, <br/>wait_for_completion, <br/>language, <br/>comment, <br/>atime_update, <br/>compression, <br/>encrypt, <br/>inline_compression, <br/>size_change_threshold, <br/>snaplock, <br/>efficiency_policy, <br/>export_policy, <br/>snapshot_policy, <br/>tiering_policy, <br/>qos_policy_group, <br/>qos_adaptive_policy_group |



## volume / decom

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Unmount volume  | netapp.ontap | na_ontap_volume |  | svm, volume |
| Set comment with timestamp on volume  | netapp.ontap | na_ontap_volume |  | , svm, volume |
| Rename volume  | netapp.ontap | na_ontap_volume |  | svm, volume |


**Variables**

| Variable | Properties |
| :------- | :--------- |
|  |  |
| svm | name |
| volume | name |



## volume / delete

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Collect cifs shares for volume  | netapp.ontap | na_ontap_rest_info |  |  |
| Remove cifs shares for volume  |  | include_tasks | x | cifs_share_info |
| Delete volume  | netapp.ontap | na_ontap_volume |  | svm, volume |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| cifs_share_info | ontap_info |
| svm | name |
| volume | name |



## volume / delete_lock

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Get locks on volume  | netapp.ontap | na_ontap_restit |  |  |
| Delete locks on volume  | netapp.ontap | na_ontap_restit | x | lock, locks_info |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| lock | uuid |
| locks_info | response |



## volume / modify

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| modify volume  | netapp.ontap | na_ontap_volume |  | svm, volume |
| Set efficiency  | netapp.ontap | na_ontap_volume_efficiency |  | svm, volume |
| Set compression type  | netapp.ontap | na_ontap_rest_cli |  |  |
| Set efficiency schedule  | netapp.ontap | na_ontap_rest_cli |  |  |
| Set volume autosize  | netapp.ontap | na_ontap_volume_autosize |  | svm, volume |
| Set volume snapshot autodelete  | netapp.ontap | na_ontap_rest_cli |  |  |
| Set space-mgmt-try-first  | netapp.ontap | na_ontap_rest_cli |  |  |
| Get volume uuid  | netapp.ontap | na_ontap_restit |  |  |
| Set anti-ransomware state  | netapp.ontap | na_ontap_restit |  | volume_info |
| Set read-alloc  | netapp.ontap | na_ontap_rest_cli |  |  |
| Set fractional-reserve  | netapp.ontap | na_ontap_rest_cli |  |  |
| Set atime-update  | netapp.ontap | na_ontap_rest_cli |  |  |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| svm | name |
| volume | name, <br/>type, <br/>is_online, <br/>activity_tracking, <br/>analytics, <br/>auto_remap_luns, <br/>junction_path, <br/>language, <br/>comment, <br/>atime_update, <br/>compression, <br/>encrypt, <br/>group_id, <br/>inline_compression, <br/>size_change_threshold, <br/>unix_permissions, <br/>user_id, <br/>security_style, <br/>snaplock, <br/>logical_space_reporting, <br/>logical_space_enforcement, <br/>efficiency_policy, <br/>export_policy, <br/>snapshot_policy, <br/>tiering_policy, <br/>qos_policy_group, <br/>qos_adaptive_policy_group, <br/>volume_efficiency, <br/>volume_autosize |
| volume_info | response |



## volume / move

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Find best aggregate  |  | get_best_aggregate |  | svm, volume |
| Move volume  | netapp.ontap | na_ontap_volume |  | svm, volume |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| svm | name |
| volume | name, <br/>size, <br/>aggregate_include_node_regex, <br/>aggregate |



## volume / offline

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Offline volume  | netapp.ontap | na_ontap_volume |  | svm, volume |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| svm | name |
| volume | name |



## volume / online

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Online volume  | netapp.ontap | na_ontap_volume |  | svm, volume |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| svm | name |
| volume | name |



## volume / rename

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Rename volume  | netapp.ontap | na_ontap_volume |  | svm, volume |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| svm | name |
| volume | old_name, <br/>name |



## volume / resize

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Resize volume  | netapp.ontap | na_ontap_volume |  | svm, volume |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| svm | name |
| volume | name, <br/>size, <br/>size_unit |




