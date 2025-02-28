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
| Mapping the lun |  | na_ontap_lun_map | x | lun, svm |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| lun | name<br>comment<br>size<br>force_resize<br>force_remove_fenced<br>os_type<br>qos_adaptive_policy_group<br>qos_policy_group<br>qtree_name<br>size_unit<br>space_allocation<br>space_reserve<br>use_exact_size<br>igroups |
| svm | name |
| volume | name |



## lun / decom

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Get lun uuid | netapp.ontap | na_ontap_restit |  |  |
| Offline lun | netapp.ontap | na_ontap_restit |  |  |
| Rename lun | netapp.ontap | na_ontap_lun |  | lun, svm, volume |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| lun | name |
| svm | name |
| volume | name |



## lun / delete

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Get lun info | netapp.ontap | na_ontap_restit |  |  |
| Get lun info | netapp.ontap | na_ontap_restit |  |  |
| Check status |  | assert |  |  |
| Get all LUN mappings | netapp.ontap | na_ontap_rest_info |  |  |
| Remove all LUN mappings | netapp.ontap | na_ontap_lun_map | x | lun_map_info |
| Delete lun | netapp.ontap | na_ontap_lun |  | lun, svm, volume |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| lun | name |
| lun_map_info | ontap_info |
| svm | name |
| volume | name |



## lun / recover

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Get lun uuid | netapp.ontap | na_ontap_restit |  |  |
| Online lun | netapp.ontap | na_ontap_restit |  |  |
| Rename lun | netapp.ontap | na_ontap_lun |  | lun, svm, volume |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| lun | name<br>original_name |
| svm | name |
| volume | name |



## lun / rename

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Rename lun {{ lun.name   }} | netapp.ontap | na_ontap_lun |  | lun, svm, volume |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| lun | name<br>new_name |
| svm | name |
| volume | name |



## lun / update

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Modify lun {{ lun.name  }} | netapp.ontap | na_ontap_lun |  | lun, svm, volume |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| lun | name<br>comment<br>size<br>force_resize<br>force_remove_fenced<br>os_type<br>qos_adaptive_policy_group<br>qos_policy_group<br>qtree_name<br>size_unit<br>space_allocation<br>space_reserve<br>use_exact_size |
| svm | name |
| volume | name |




