# ontap / vlan 
Manage NetApp ONTAP VLANs  
  
Note : This role supports multi / looping





## Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [create](#vlan--create) |  |



## vlan / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Create VLAN | netapp.ontap | na_ontap_net_vlan |  | vlan |
| Initialize ports list |  | set_fact |  |  |
| Accumulate ports in the list |  | set_fact | x |  |
| Add VLAN ports to broadcast domain | netapp.ontap | na_ontap_broadcast_domain |  | vlan |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| vlan | tag, <br/>port, <br/>node, <br/>broadcast_domain, <br/>ipspace, <br/>ports |




