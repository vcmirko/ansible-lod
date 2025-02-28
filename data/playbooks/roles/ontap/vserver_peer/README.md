# ontap / vserver_peer 
Manage NetApp ONTAP Vserver Peers  
  






## Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [create](#vserver_peer--create) |  |



## vserver_peer / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Create vserver peering  | netapp.ontap | na_ontap_vserver_peer |  | vserver_peer[0], vserver_peer[1] |
| wait for vserver peering to be established |  | pause |  |  |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| vserver_peer[0] | svm |
| vserver_peer[1] | svm<br>cluster |




