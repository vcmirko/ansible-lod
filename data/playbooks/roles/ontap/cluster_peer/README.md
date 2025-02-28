# ontap / cluster_peer 
Manage NetApp ONTAP Cluster Peer  
  






## Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [create](#cluster_peer--create) |  |



## cluster_peer / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Create cluster peering between {{ cluster_peer.name }} | netapp.ontap | na_ontap_cluster_peer |  | cluster_peer[0], cluster_peer[1] |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| cluster_peer[0] | intercluster_ips<br>passphrase |
| cluster_peer[1] | intercluster_ips |




