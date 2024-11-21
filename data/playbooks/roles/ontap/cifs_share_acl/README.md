# Tasks Summary

## create.yml
This file supports the following properties:

### cluster
| Property       | Description                                |
|----------------|--------------------------------------------|
| **name**       | The name of the cluster.                   |

### svm
| Property       | Description                                |
|----------------|--------------------------------------------|
| **name**       | The name of the SVM.                       |

### cifs_share_acl
| Property       | Description                                |
|----------------|--------------------------------------------|
| **share_name** | The name of the CIFS share.                |
| **user_or_group** | The user or group for the ACL.          |
| **permission** | The permission level for the ACL.          |
| **type**       | The type of the ACL (e.g., allow, deny).   |
| **state**      | The state of the ACL (e.g., present, absent). |