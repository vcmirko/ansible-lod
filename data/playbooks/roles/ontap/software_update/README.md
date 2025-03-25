# ontap / software_update 
Manage NetApp ONTAP Software Updates  
  






## Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [download](#software_update--download) |  |
| [firmware_update](#software_update--firmware_update) |  |
| [remove](#software_update--remove) |  |
| [update](#software_update--update) |  |



## software_update / download

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Downloading software on  |  | na_ontap_software_update |  | software |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| software | baseurl \nfilename |



## software_update / firmware_update

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |


**Variables**

| Variable | Properties |
| :------- | :--------- |



## software_update / remove

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Removing software on  |  | na_ontap_software_update |  | software |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| software | version |



## software_update / update

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Set maintenance hours |  | set_fact |  |  |
| Enable maintenance in aiqum |  | include_tasks |  |  |
| Get all ip interfaces not home | netapp.ontap | na_ontap_rest_info |  |  |
| Revert ip interfaces to home |  | na_ontap_interface | x | lif_info |
| Invoke Autosupport - MAINTENANCE START | netapp.ontap | na_ontap_autosupport_invoke |  | software |
| Update Software |  | na_ontap_software_update |  | software |
| Invoke Autosupport - MAINTENANCE END | netapp.ontap | na_ontap_autosupport_invoke |  | software |
| End maintenance in aiqum |  | include_tasks |  |  |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| lif_info | ontap_info |
| software | version \nignore_validation_warning |




