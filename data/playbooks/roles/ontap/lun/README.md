# ontap / lun 
Manage NetApp ONTAP LUNs  
  
Note : This role supports multi / looping





## Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [create](#lun--create) |  |
| [decom](#lun--decom) |  |
| [delete](#lun--delete) |  |
| [recover](#lun--recover) |  |
| [rename](#lun--rename) |  |
| [update](#lun--update) |  |



## lun / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Create/Modify Lun  | netapp.ontap | na_ontap_lun |  | lun, svm, volume |
| Mapping the lun |  | na_ontap_lun_map | x | lun, svm, volume |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| lun | name \ncomment \nsize \nforce_resize \nforce_remove_fenced \nos_type \nqos_adaptive_policy_group \nqos_policy_group \nqtree_name \nsize_unit \nspace_allocation \nspace_reserve \nuse_exact_size \nigroups |
| svm | name |
| volume | name |



## lun / decom

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Get lun uuid | netapp.ontap | na_ontap_restit |  |  |
| Offline lun | netapp.ontap | na_ontap_restit |  | lun_info |
| Rename lun | netapp.ontap | na_ontap_lun |  | lun, svm, volume |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| lun | name |
| lun_info | response |
| svm | name |
| volume | name |



## lun / delete

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Get lun info | netapp.ontap | na_ontap_restit |  |  |
| Get lun info | netapp.ontap | na_ontap_restit |  | lun_uuid |
| Check status |  | assert |  |  |
| Get all LUN mappings | netapp.ontap | na_ontap_rest_info |  |  |
| Remove all LUN mappings | netapp.ontap | na_ontap_lun_map | x | lun_map_info |
| Delete lun | netapp.ontap | na_ontap_lun |  | lun, svm, volume |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| lun | name |
| lun_map_info | ontap_info |
| lun_uuid | response |
| svm | name |
| volume | name |



## lun / recover

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Get lun uuid | netapp.ontap | na_ontap_restit |  |  |
| Online lun | netapp.ontap | na_ontap_restit |  | lun_info |
| Rename lun | netapp.ontap | na_ontap_lun |  | lun, svm, volume |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| lun | name \noriginal_name |
| lun_info | response |
| svm | name |
| volume | name |



## lun / rename

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Rename lun {{ lun.name   }} | netapp.ontap | na_ontap_lun |  | lun, svm, volume |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| lun | name \nnew_name |
| svm | name |
| volume | name |



## lun / update

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Modify lun {{ lun.name  }} | netapp.ontap | na_ontap_lun |  | lun, svm, volume |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| lun | name \ncomment \nsize \nforce_resize \nforce_remove_fenced \nos_type \nqos_adaptive_policy_group \nqos_policy_group \nqtree_name \nsize_unit \nspace_allocation \nspace_reserve \nuse_exact_size |
| svm | name |
| volume | name |




