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

### cluster_peer
This is a 2-item list where the first entry is the source cluster and the second entry is the destination cluster.

| Property       | Description                                |
|----------------|--------------------------------------------|
| **name**       | The name of the peer cluster.              |
| **intercluster_ips** | The intercluster IPs of the peer cluster. |
| **management_ip** | The management IP of the peer cluster.  |
| **username**   | The username for the peer cluster.         |
| **password**   | The password for the peer cluster.         |
| **passphrase** | The passphrase for the peer cluster.       |