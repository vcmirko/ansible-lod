# ontap / nfs 
Manage NetApp ONTAP NFS Servers  
  






## Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [create](#nfs--create) |  |



## nfs / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Enable nfs | netapp.ontap | na_ontap_nfs |  | nfs, svm |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| nfs | showmount, <br/>nfsv3, <br/>nfsv3_fsid_change, <br/>nfsv4, <br/>nfsv41, <br/>nfsv41_acl, <br/>nfsv41_pnfs, <br/>tcp_max_xfer_size, <br/>nfsv4_id_domain, <br/>vstorage_state |
| svm | name |




