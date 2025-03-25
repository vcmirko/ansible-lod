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
| nfs | showmount \nnfsv3 \nnfsv3_fsid_change \nnfsv4 \nnfsv41 \nnfsv41_acl \nnfsv41_pnfs \ntcp_max_xfer_size \nnfsv4_id_domain \nvstorage_state |
| svm | name |




