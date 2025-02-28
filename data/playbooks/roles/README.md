# Collections
This folder contains the collections of roles that are used to deploy the different components of the platform.

| Collection | Description |
| :--- | :---------- |
| [aiqum](#aiqum) | Netapp AIQUM (Active IQ Unified Manager) integration |
| [awx](#awx) | AWX (Ansible Tower / Ansible Automation Platform) integration |
| [cyberark](#cyberark) | CyberArk integration |
| [eeod](#eeod) | Netapp EEOD (Epic Environment on Demand) integration |
| [infoblox](#infoblox) | Infoblox integration |
| [maf](#maf) | MAF - Modular Ansible Framework - this current framework, some common roles |
| [ontap](#ontap) | Netapp ONTAP integration |



## aiqum
Netapp AIQUM (Active IQ Unified Manager) integration

| Roles | Description |
| :--- | :--- |
| maintenance | Start, stop AIQUM maintenance |
| management | AIQUM management, register, rediscover, ... |



## awx
AWX (Ansible Tower / Ansible Automation Platform) integration

| Roles | Description |
| :--- | :--- |
| job | Manages AWX job tasks |



## cyberark
CyberArk integration

| Roles | Description |
| :--- | :--- |
| pam | Manages CyberArk PAM tasks |



## eeod
Netapp EEOD (Epic Environment on Demand) integration

| Roles | Description |
| :--- | :--- |
| logic | EEOD Logic, import excel file to deploy luns |



## infoblox
Infoblox integration

| Roles | Description |
| :--- | :--- |
| ip_management | Manage IP addresses in Infoblox |



## maf
MAF - Modular Ansible Framework - this current framework, some common roles

| Roles | Description |
| :--- | :--- |
| facts | Process sample credentials for MAF testing |
| logic | -- Missing description -- |



## ontap
Netapp ONTAP integration

| Roles | Description |
| :--- | :--- |
| cifs | Manage NetApp ONTAP CIFS server |
| cifs_local_group | Manage NetApp ONTAP CIFS local groups |
| cifs_local_user | Manage NetApp ONTAP CIFS local users |
| cifs_privilege | Manage NetApp ONTAP Cifs Privileges |
| cifs_share | Manage NetApp ONTAP CIFS shares |
| cifs_share_acl | Manage NetApp ONTAP CIFS share ACLs |
| cluster | Manage NetApp ONTAP Cluster |
| cluster_peer | Manage NetApp ONTAP Cluster Peer |
| dns | Manage NetApp ONTAP DNS |
| export_policy | Manage NetApp ONTAP Export Policies and rules |
| facts | Manage NetApp ONTAP Facts, like validations |
| file_security_permissions | Manage NetApp ONTAP File Security Permissions |
| firmware_upgrade | Manage NetApp ONTAP Firmware Upgrades |
| iscsi | Manage NetApp ONTAP iSCSI Servers |
| lif | Manage NetApp ONTAP Logical Interfaces (LIFs) |
| lun | Manage NetApp ONTAP LUNs |
| name_mapping | Manage NetApp ONTAP Name Mappings |
| nfs | Manage NetApp ONTAP NFS Servers |
| qos_policy_group | Manage NetApp ONTAP QoS Policy Groups |
| qtree | Manage NetApp ONTAP Qtrees |
| quota | Manage NetApp ONTAP Quotas |
| quota_policy | Manage NetApp ONTAP Quota Policies |
| security_certificate | Manage NetApp ONTAP Security Certificates |
| snapmirror | Manage NetApp ONTAP Snapmirrors |
| snapmirror_policy | Manage NetApp ONTAP SnapMirror policies |
| snapshot_policy | Manage NetApp ONTAP Snapshot Policies |
| software_update | Manage NetApp ONTAP Software Updates |
| subnet | Manage NetApp ONTAP Subnets |
| svm | Manage NetApp ONTAP SVMs (vservers) |
| unix_group | Manage NetApp ONTAP Unix Groups |
| unix_user | Manage NetApp ONTAP Unix Users |
| user | Manage NetApp ONTAP Users |
| vlan | Manage NetApp ONTAP VLANs |
| volume | Manage NetApp ONTAP volumes |
| vscan_scanner_pool | Manage NetApp ONTAP Vscan Scanner Pools |
| vserver_peer | Manage NetApp ONTAP Vserver Peers |




