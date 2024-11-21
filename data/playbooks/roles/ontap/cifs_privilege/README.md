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

### cifs_privilege
| Property       | Description                                |
|----------------|--------------------------------------------|
| **name**       | The name of the CIFS privilege.            |
| **privileges** | A list of privileges assigned to the CIFS user. |

### privilege
This dictionary is used within the `cifs_privilege.privileges` list.

| Property       | Description                                |
|----------------|--------------------------------------------|
| **name**       | The name of the privilege.                 |