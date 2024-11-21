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

### cifs_share
| Property                   | Description                                |
|----------------------------|--------------------------------------------|
| **name**                   | The name of the CIFS share.                |
| **path**                   | The path of the CIFS share.                |
| **comment**                | The comment for the CIFS share.            |
| **access_based_enumeration**| Whether access-based enumeration is enabled. |
| **show_snapshot**          | Whether to show snapshots.                 |
| **show_previous_versions** | Whether to show previous versions.         |
| **oplocks**                | Whether opportunistic locking is enabled.  |
| **home_directory**         | Whether the share is a home directory.     |
| **change_notify**          | The change notify setting.                 |
| **encryption**             | Whether encryption is enabled.             |
| **namespace_caching**      | Whether namespace caching is enabled.      |
| **continuously_available** | Whether the share is continuously available. |
| **cifs_browsable**         | Whether the share is browsable.            |
| **allow_unencrypted_access**| Whether to allow unencrypted access.      |
| **unix_symlink**           | Whether Unix symlink is enabled.           |
| **vscan_profile**          | The Vscan profile for the CIFS share.      |
| **acls**                   | A list of ACLs for the CIFS share.         |

### acl
This dictionary is used within the `cifs_share.acls` list.

| Property       | Description                                |
|----------------|--------------------------------------------|
| **state**      | The state of the ACL (e.g., present, absent). |
| **user_or_group** | The user or group for the ACL.          |
| **permission** | The permission level for the ACL.          |
| **acl_type**   | The type of the ACL (e.g., allow, deny).   |