# ontap
Netapp ONTAP integration

| Role | Description |
| :--- | :---------- |
| [cifs](#ontap--cifs) | Manage NetApp ONTAP CIFS server |
| [cifs_local_group](#ontap--cifs_local_group) | Manage NetApp ONTAP CIFS local groups |
| [cifs_local_user](#ontap--cifs_local_user) | Manage NetApp ONTAP CIFS local users |
| [cifs_privilege](#ontap--cifs_privilege) | Manage NetApp ONTAP Cifs Privileges |
| [cifs_share](#ontap--cifs_share) | Manage NetApp ONTAP CIFS shares |
| [cifs_share_acl](#ontap--cifs_share_acl) | Manage NetApp ONTAP CIFS share ACLs |
| [cluster](#ontap--cluster) | Manage NetApp ONTAP Cluster |
| [cluster_peer](#ontap--cluster_peer) | Manage NetApp ONTAP Cluster Peer |
| [dns](#ontap--dns) | Manage NetApp ONTAP DNS |
| [export_policy](#ontap--export_policy) | Manage NetApp ONTAP Export Policies and rules |
| [facts](#ontap--facts) | Manage NetApp ONTAP Facts, like validations |
| [file_security_permissions](#ontap--file_security_permissions) | Manage NetApp ONTAP File Security Permissions |
| [firmware_upgrade](#ontap--firmware_upgrade) | Manage NetApp ONTAP Firmware Upgrades |
| [iscsi](#ontap--iscsi) | Manage NetApp ONTAP iSCSI Servers |
| [lif](#ontap--lif) | Manage NetApp ONTAP Logical Interfaces (LIFs) |
| [lun](#ontap--lun) | Manage NetApp ONTAP LUNs |
| [name_mapping](#ontap--name_mapping) | Manage NetApp ONTAP Name Mappings |
| [nfs](#ontap--nfs) | Manage NetApp ONTAP NFS Servers |
| [qos_policy_group](#ontap--qos_policy_group) | Manage NetApp ONTAP QoS Policy Groups |
| [qtree](#ontap--qtree) | Manage NetApp ONTAP Qtrees |
| [quota](#ontap--quota) | Manage NetApp ONTAP Quotas |
| [quota_policy](#ontap--quota_policy) | Manage NetApp ONTAP Quota Policies |
| [security_certificate](#ontap--security_certificate) | Manage NetApp ONTAP Security Certificates |
| [snapmirror](#ontap--snapmirror) | Manage NetApp ONTAP Snapmirrors |
| [snapmirror_policy](#ontap--snapmirror_policy) | Manage NetApp ONTAP SnapMirror policies |
| [snapshot_policy](#ontap--snapshot_policy) | Manage NetApp ONTAP Snapshot Policies |
| [software_update](#ontap--software_update) | Manage NetApp ONTAP Software Updates |
| [subnet](#ontap--subnet) | Manage NetApp ONTAP Subnets |
| [svm](#ontap--svm) | Manage NetApp ONTAP SVMs (vservers) |
| [unix_group](#ontap--unix_group) | Manage NetApp ONTAP Unix Groups |
| [unix_user](#ontap--unix_user) | Manage NetApp ONTAP Unix Users |
| [user](#ontap--user) | Manage NetApp ONTAP Users |
| [vlan](#ontap--vlan) | Manage NetApp ONTAP VLANs |
| [volume](#ontap--volume) | Manage NetApp ONTAP volumes |
| [vscan_scanner_pool](#ontap--vscan_scanner_pool) | Manage NetApp ONTAP Vscan Scanner Pools |
| [vserver_peer](#ontap--vserver_peer) | Manage NetApp ONTAP Vserver Peers |



## ontap / cifs

Manage NetApp ONTAP CIFS server  
  






### Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [create](#cifs--create) |  |
| [delete](#cifs--delete) |  |
| [stop](#cifs--stop) |  |



### cifs / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Enable cifs | netapp.ontap | na_ontap_cifs_server |  | ad_password, ad_username, cifs, svm |
| Set cifs options - no rest equivalent | netapp.ontap | na_ontap_rest_cli |  |  |
| Create cifs privileges | netapp.ontap | na_ontap_restit | x | cifs |
| Remove unwanted admins | netapp.ontap | na_ontap_cifs_local_group_member | x | cifs, svm |
| Add extra admins | netapp.ontap | na_ontap_cifs_local_group_member | x | cifs, svm |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| ad_password |  |
| ad_username |  |
| cifs | name, <br/>domain, <br/>ou, <br/>session_security, <br/>smb_encryption, <br/>smb_signing, <br/>try_ldap_channel_binding, <br/>restrict_anonymous, <br/>lm_compatibility_level, <br/>ldap_referral_enabled, <br/>kdc_encryption, <br/>is_multichannel_enabled, <br/>encrypt_dc_connection, <br/>default_site, <br/>aes_netlogon_enabled, <br/>privileges, <br/>administrators |
| svm | name |



### cifs / delete

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Remove cifs | netapp.ontap | na_ontap_cifs_server |  | cifs, svm |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| cifs | name |
| svm | name |



### cifs / stop

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Stop cifs | netapp.ontap | na_ontap_cifs_server |  | cifs, svm |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| cifs | name |
| svm | name |







## ontap / cifs_local_group

Manage NetApp ONTAP CIFS local groups  
  
Note : This role supports multi / looping





### Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [add](#cifs_local_group--add) |  |
| [create](#cifs_local_group--create) |  |
| [delete](#cifs_local_group--delete) |  |



### cifs_local_group / add

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Add Cifs Local User To Group  | netapp.ontap | na_ontap_cifs_local_group_member | x | cifs_local_group, svm |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| cifs_local_group | name, <br/>members |
| svm | name |



### cifs_local_group / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Create cifs local group  | netapp.ontap | na_ontap_cifs_local_group |  | cifs_local_group, svm |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| cifs_local_group | name |
| svm | name |



### cifs_local_group / delete

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Delete cifs local group  | netapp.ontap | na_ontap_cifs_local_group |  | cifs_local_group, svm |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| cifs_local_group | name |
| svm | name |







## ontap / cifs_local_user

Manage NetApp ONTAP CIFS local users  
  
Note : This role supports multi / looping





### Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [create](#cifs_local_user--create) |  |



### cifs_local_user / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Create cifs local user  | netapp.ontap | na_ontap_cifs_local_user |  | cifs_local_user, svm |
| Add Cifs Local User  | netapp.ontap | na_ontap_cifs_local_group_member |  | cifs_local_group, cifs_local_user, svm |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| cifs_local_group | name |
| cifs_local_user | name, <br/>password, <br/>full_name, <br/>account_disabled, <br/>description |
| svm | name |







## ontap / cifs_privilege

Manage NetApp ONTAP Cifs Privileges  
  






### Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [create](#cifs_privilege--create) |  |



### cifs_privilege / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Setting cifs privilege  | netapp.ontap | na_ontap_restit |  |  |


**Variables**

| Variable | Properties |
| :------- | :--------- |







## ontap / cifs_share

Manage NetApp ONTAP CIFS shares  
  
Note : This role supports multi / looping





### Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [create](#cifs_share--create) |  |
| [delete](#cifs_share--delete) |  |



### cifs_share / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Create Cifs Share  | netapp.ontap | na_ontap_cifs |  | cifs_share, svm |
| Get cifs share uuid | netapp.ontap | na_ontap_restit |  |  |
| Set Vscan Profile for Cifs Share  | netapp.ontap | na_ontap_restit |  | cifs_share, cifs_share_info |
| Setting Cifs Share ACLs | netapp.ontap | na_ontap_cifs_acl | x | cifs_share, svm |
| Setting file security permissions for Cifs Share  | netapp.ontap | na_ontap_file_security_permissions |  | cifs_share, svm |
| Setting file security permissions acl for Cifs Share  | netapp.ontap | na_ontap_file_security_permissions_acl | x | cifs_share, svm |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| cifs_share | name, <br/>path, <br/>comment, <br/>access_based_enumeration, <br/>show_snapshot, <br/>show_previous_versions, <br/>oplocks, <br/>home_directory, <br/>change_notify, <br/>encryption, <br/>namespace_caching, <br/>continuously_available, <br/>browsable, <br/>allow_unencrypted_access, <br/>unix_symlink, <br/>acls, <br/>file_security_permissions, <br/>file_security_permissions_acls |
| cifs_share_info | response |
| svm | name |



### cifs_share / delete

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Delete Cifs Share  | netapp.ontap | na_ontap_cifs |  | cifs_share, svm |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| cifs_share | name |
| svm | name |







## ontap / cifs_share_acl

Manage NetApp ONTAP CIFS share ACLs  
  
Note : This role supports multi / looping





### Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [create](#cifs_share_acl--create) |  |



### cifs_share_acl / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| {{ task_action}} Cifs Share ACL  | netapp.ontap | na_ontap_cifs_acl |  | cifs_share_acl, svm |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| cifs_share_acl | state, <br/>share_name, <br/>user_or_group, <br/>permission, <br/>type |
| svm | name |







## ontap / cluster

Manage NetApp ONTAP Cluster  
  






### Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [create_api_user](#cluster--create_api_user) |  |
| [example_report](#cluster--example_report) |  |
| [test_api_user](#cluster--test_api_user) |  |



### cluster / create_api_user

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| check if the certificate exists |  | stat |  | cluster_api_cert_filepath |
| get expiry days from certificate |  | set_fact |  |  |
| renew the certificate if the expiry date is due to renewal |  | block |  |  |
| create the api user | netapp.ontap | na_ontap_user |  | cluster_api_role, cluster_api_username, netapp_hostname, netapp_password, netapp_username |
| test the api user | netapp.ontap | na_ontap_rest_info |  | cluster_api_cert_filepath, cluster_api_key_filepath, netapp_hostname |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| cluster_api_cert_filepath |  |
| cluster_api_key_filepath |  |
| cluster_api_role |  |
| cluster_api_username |  |
| netapp_hostname |  |
| netapp_password |  |
| netapp_username |  |



### cluster / example_report

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| get cluster info | netapp.ontap | na_ontap_rest_info |  |  |
| Print cluster info |  | debug |  |  |


**Variables**

| Variable | Properties |
| :------- | :--------- |



### cluster / test_api_user

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| test the api user | netapp.ontap | na_ontap_rest_info |  | cluster_api_cert_filepath, cluster_api_key_filepath, netapp_hostname |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| cluster_api_cert_filepath |  |
| cluster_api_key_filepath |  |
| netapp_hostname |  |







## ontap / cluster_peer

Manage NetApp ONTAP Cluster Peer  
  






### Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [create](#cluster_peer--create) |  |



### cluster_peer / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Create cluster peering between {{ cluster_peer.name }} | netapp.ontap | na_ontap_cluster_peer |  | cluster_peer |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| cluster_peer |  |







## ontap / dns

Manage NetApp ONTAP DNS  
  






### Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [create](#dns--create) |  |



### dns / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| create dns | netapp.ontap | na_ontap_dns |  | dns, svm |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| dns | domains, <br/>servers, <br/>skip_validation |
| svm | name |







## ontap / export_policy

Manage NetApp ONTAP Export Policies and rules  
  






### Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [create](#export_policy--create) |  |
| [delete](#export_policy--delete) |  |



### export_policy / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Create Export Policy | netapp.ontap | na_ontap_export_policy |  | export_policy, svm |
| Create/Delete/Modify export rules | netapp.ontap | na_ontap_export_policy_rule | x | export_policy, svm |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| export_policy | name, <br/>rules |
| svm | name |



### export_policy / delete

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Delete Export Policy | netapp.ontap | na_ontap_export_policy |  | export_policy, svm |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| export_policy | name |
| svm | name |







## ontap / facts

Manage NetApp ONTAP Facts, like validations  
  






### Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [validate](#facts--validate) |  |



### facts / validate

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| check ontap credentials |  | assert |  |  |


**Variables**

| Variable | Properties |
| :------- | :--------- |







## ontap / file_security_permissions

Manage NetApp ONTAP File Security Permissions  
  






### Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [create](#file_security_permissions--create) |  |



### file_security_permissions / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Setting NTFS DACL  | netapp.ontap | na_ontap_file_security_permissions |  | file_security_permissions, svm |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| file_security_permissions | access_control, <br/>path, <br/>owner, <br/>acls |
| svm | name |







## ontap / firmware_upgrade

Manage NetApp ONTAP Firmware Upgrades  
  






### Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [upgrade](#firmware_upgrade--upgrade) |  |



### firmware_upgrade / upgrade

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Update disk fw |  | na_ontap_firmware_upgrade |  | firmware |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| firmware | baseurl, <br/>filename |







## ontap / iscsi

Manage NetApp ONTAP iSCSI Servers  
  






### Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [create](#iscsi--create) |  |



### iscsi / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Enable iscsi | netapp.ontap | na_ontap_iscsi |  | iscsi, svm |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| iscsi | target_alias |
| svm | name |







## ontap / lif

Manage NetApp ONTAP Logical Interfaces (LIFs)  
  






### Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [create](#lif--create) |  |
| [delete](#lif--delete) |  |
| [migrate](#lif--migrate) |  |



### lif / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| create lif  | netapp.ontap | na_ontap_interface |  | ipspace, lif, svm |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| ipspace | name |
| lif | address, <br/>name, <br/>interface_type, <br/>node, <br/>port, <br/>subnet_name, <br/>is_auto_revert, <br/>is_dns_update_enabled, <br/>netmask, <br/>service_policy |
| svm | name |



### lif / delete

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| delete lif  | netapp.ontap | na_ontap_interface |  | lif, svm |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| lif | name |
| svm | name |



### lif / migrate

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| migrate lif  | netapp.ontap | na_ontap_interface |  | lif, svm |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| lif | name, <br/>node, <br/>port |
| svm | name |







## ontap / lun

Manage NetApp ONTAP LUNs  
  
Note : This role supports multi / looping





### Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [create](#lun--create) |  |
| [decom](#lun--decom) |  |
| [delete](#lun--delete) |  |
| [recover](#lun--recover) |  |
| [rename](#lun--rename) |  |
| [update](#lun--update) |  |



### lun / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Create/Modify Lun  | netapp.ontap | na_ontap_lun |  | lun, svm, volume |
| Mapping the lun |  | na_ontap_lun_map | x | lun, svm, volume |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| lun | name, <br/>comment, <br/>size, <br/>force_resize, <br/>force_remove_fenced, <br/>os_type, <br/>qos_adaptive_policy_group, <br/>qos_policy_group, <br/>qtree_name, <br/>size_unit, <br/>space_allocation, <br/>space_reserve, <br/>use_exact_size, <br/>igroups |
| svm | name |
| volume | name |



### lun / decom

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Get lun uuid | netapp.ontap | na_ontap_restit |  |  |
| Offline lun | netapp.ontap | na_ontap_restit |  | lun_info |
| Rename lun | netapp.ontap | na_ontap_lun |  | lun, svm, volume |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| lun | name |
| lun_info | response |
| svm | name |
| volume | name |



### lun / delete

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Get lun info | netapp.ontap | na_ontap_restit |  |  |
| Get lun info | netapp.ontap | na_ontap_restit |  | lun_uuid |
| Check status |  | assert |  |  |
| Get all LUN mappings | netapp.ontap | na_ontap_rest_info |  |  |
| Remove all LUN mappings | netapp.ontap | na_ontap_lun_map | x | lun_map_info |
| Delete lun | netapp.ontap | na_ontap_lun |  | lun, svm, volume |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| lun | name |
| lun_map_info | ontap_info |
| lun_uuid | response |
| svm | name |
| volume | name |



### lun / recover

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Get lun uuid | netapp.ontap | na_ontap_restit |  |  |
| Online lun | netapp.ontap | na_ontap_restit |  | lun_info |
| Rename lun | netapp.ontap | na_ontap_lun |  | lun, svm, volume |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| lun | name, <br/>original_name |
| lun_info | response |
| svm | name |
| volume | name |



### lun / rename

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Rename lun {{ lun.name   }} | netapp.ontap | na_ontap_lun |  | lun, svm, volume |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| lun | name, <br/>new_name |
| svm | name |
| volume | name |



### lun / update

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Modify lun {{ lun.name  }} | netapp.ontap | na_ontap_lun |  | lun, svm, volume |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| lun | name, <br/>comment, <br/>size, <br/>force_resize, <br/>force_remove_fenced, <br/>os_type, <br/>qos_adaptive_policy_group, <br/>qos_policy_group, <br/>qtree_name, <br/>size_unit, <br/>space_allocation, <br/>space_reserve, <br/>use_exact_size |
| svm | name |
| volume | name |







## ontap / name_mapping

Manage NetApp ONTAP Name Mappings  
  






### Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [create](#name_mapping--create) |  |



### name_mapping / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Create Name Mapping | netapp.ontap | na_ontap_name_mappings |  | name_mapping, svm |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| name_mapping | direction, <br/>index, <br/>pattern, <br/>replacement, <br/>client_match |
| svm | name |







## ontap / nfs

Manage NetApp ONTAP NFS Servers  
  






### Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [create](#nfs--create) |  |



### nfs / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Enable nfs | netapp.ontap | na_ontap_nfs |  | nfs, svm |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| nfs | showmount, <br/>nfsv3, <br/>nfsv3_fsid_change, <br/>nfsv4, <br/>nfsv41, <br/>nfsv41_acl, <br/>nfsv41_pnfs, <br/>tcp_max_xfer_size, <br/>nfsv4_id_domain, <br/>vstorage_state |
| svm | name |







## ontap / qos_policy_group

Manage NetApp ONTAP QoS Policy Groups  
  






### Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [create](#qos_policy_group--create) |  |



### qos_policy_group / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Create QOS Policy Group  | netapp.ontap | na_ontap_qos_policy_group |  | qos_policy_group, svm |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| qos_policy_group | name, <br/>fixed_qos_options |
| svm | name |







## ontap / qtree

Manage NetApp ONTAP Qtrees  
  
Note : This role supports multi / looping





### Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [create](#qtree--create) |  |



### qtree / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| create qtree  | netapp.ontap | na_ontap_qtree |  | qtree, svm, volume |
| Set qtree oplocks  | netapp.ontap | na_ontap_rest_cli |  |  |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| qtree | name, <br/>export_policy, <br/>security_style, <br/>unix_permissions, <br/>unix_group, <br/>unix_user, <br/>wait_for_completion |
| svm | name |
| volume | name |







## ontap / quota

Manage NetApp ONTAP Quotas  
  
Note : This role supports multi / looping





### Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [create](#quota--create) |  |
| [delete](#quota--delete) |  |
| [off_on](#quota--off_on) |  |



### quota / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Create/Modify Quota  | netapp.ontap | na_ontap_quotas |  | quota, svm, volume |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| quota | quota_target, <br/>disk_limit, <br/>file_limit, <br/>perform_user_mapping, <br/>qtree, <br/>set_quota_status, <br/>soft_disk_limit, <br/>soft_file_limit, <br/>threshold, <br/>type |
| svm | name |
| volume | name |



### quota / delete

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Delete Quota on  | netapp.ontap | na_ontap_quotas |  | quota, svm, volume |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| quota | quota_target, <br/>disk_limit, <br/>file_limit, <br/>perform_user_mapping, <br/>qtree, <br/>set_quota_status, <br/>soft_disk_limit, <br/>soft_file_limit, <br/>threshold, <br/>type |
| svm | name |
| volume | name |



### quota / off_on

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Set Quota off ->  | netapp.ontap | na_ontap_quotas |  | svm, volume |
| Set Quota on ->  | netapp.ontap | na_ontap_quotas |  | svm, volume |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| svm | name |
| volume | name |







## ontap / quota_policy

Manage NetApp ONTAP Quota Policies  
  






### Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [create](#quota_policy--create) |  |
| [delete](#quota_policy--delete) |  |
| [set](#quota_policy--set) |  |



### quota_policy / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Create/Modify Quota Policy  |  | na_ontap_rest_cli_idempotent |  |  |


**Variables**

| Variable | Properties |
| :------- | :--------- |



### quota_policy / delete

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Delete Quota Policy  |  | na_ontap_rest_cli_idempotent |  |  |
| Fail on non-duplicate error |  | fail |  |  |


**Variables**

| Variable | Properties |
| :------- | :--------- |



### quota_policy / set

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Set Quota Policy  |  | na_ontap_rest_cli_idempotent |  |  |


**Variables**

| Variable | Properties |
| :------- | :--------- |







## ontap / security_certificate

Manage NetApp ONTAP Security Certificates  
  






### Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [renew](#security_certificate--renew) |  |



### security_certificate / renew

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Renew certificate |  | na_ontap_certificate_renew |  | security_certificate, svm |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| security_certificate | days, <br/>expiry_days |
| svm | name |







## ontap / snapmirror

Manage NetApp ONTAP Snapmirrors  
  
Note : This role supports multi / looping





### Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [create](#snapmirror--create) |  |
| [delete](#snapmirror--delete) |  |
| [set_retention](#snapmirror--set_retention) |  |
| [update](#snapmirror--update) |  |
| [wait_for_condition](#snapmirror--wait_for_condition) |  |



### snapmirror / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Create Snapmirror  | netapp.ontap | na_ontap_snapmirror |  | snapmirror |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| snapmirror | schedule, <br/>policy, <br/>identity_preservation, <br/>max_transfer_rate |



### snapmirror / delete

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Modify policy SnapMirror (bug fix) - to allow snapmirror break | netapp.ontap | na_ontap_snapmirror |  |  |
| Removing snapmirror  | netapp.ontap | na_ontap_snapmirror |  |  |


**Variables**

| Variable | Properties |
| :------- | :--------- |



### snapmirror / set_retention

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Get snapshot info | netapp.ontap | na_ontap_rest_info |  |  |
| Extract oldest create_date |  | set_fact |  |  |
| diff date |  | set_fact |  |  |
| Calculate keep_days |  | set_fact |  |  |
| Calculate expiration_date |  | set_fact |  |  |
| Changing comment with expiration date | netapp.ontap | na_ontap_volume |  | expiration_date, snapmirror |
| Renaming volume  | netapp.ontap | na_ontap_volume |  | snapmirror |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| expiration_date |  |
| snapmirror | destination |



### snapmirror / update

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Update Snapmirror  | netapp.ontap | na_ontap_snapmirror |  |  |


**Variables**

| Variable | Properties |
| :------- | :--------- |



### snapmirror / wait_for_condition

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Sleep for 10 seconds |  | pause |  |  |
| Wait for Snapmirror  | netapp.ontap | na_ontap_wait_for_condition |  | auth_rest_validate_certs |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| auth_rest_validate_certs |  |







## ontap / snapmirror_policy

Manage NetApp ONTAP SnapMirror policies  
  






### Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [create](#snapmirror_policy--create) |  |



### snapmirror_policy / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Create Snapmirror Policy  | netapp.ontap | na_ontap_snapmirror_policy |  | snapmirror, svm |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| snapmirror | policy_name, <br/>policy_snapmirror_label, <br/>policy_keep |
| svm | name |







## ontap / snapshot_policy

Manage NetApp ONTAP Snapshot Policies  
  






### Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [create](#snapshot_policy--create) |  |



### snapshot_policy / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Create Snapshot Policy  | netapp.ontap | na_ontap_snapshot_policy |  | snapshot_policy, svm |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| snapshot_policy | name, <br/>schedule, <br/>snapmirror_label, <br/>prefix, <br/>count, <br/>enabled |
| svm | name |







## ontap / software_update

Manage NetApp ONTAP Software Updates  
  






### Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [download](#software_update--download) |  |
| [firmware_update](#software_update--firmware_update) |  |
| [remove](#software_update--remove) |  |
| [update](#software_update--update) |  |



### software_update / download

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Downloading software on  |  | na_ontap_software_update |  | software |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| software | baseurl, <br/>filename |



### software_update / firmware_update

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |


**Variables**

| Variable | Properties |
| :------- | :--------- |



### software_update / remove

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Removing software on  |  | na_ontap_software_update |  | software |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| software | version |



### software_update / update

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Set maintenance hours |  | set_fact |  |  |
| Enable maintenance in aiqum |  | include_tasks |  |  |
| Get all ip interfaces not home | netapp.ontap | na_ontap_rest_info |  |  |
| Revert ip interfaces to home |  | na_ontap_interface | x | lif_info |
| Invoke Autosupport - MAINTENANCE START | netapp.ontap | na_ontap_autosupport_invoke |  | software |
| Update Software |  | na_ontap_software_update |  | software |
| Invoke Autosupport - MAINTENANCE END | netapp.ontap | na_ontap_autosupport_invoke |  | software |
| End maintenance in aiqum |  | include_tasks |  |  |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| lif_info | ontap_info |
| software | version, <br/>ignore_validation_warning |







## ontap / subnet

Manage NetApp ONTAP Subnets  
  






### Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [create](#subnet--create) |  |



### subnet / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Create Subnet  | netapp.ontap | na_ontap_net_subnet |  | subnet |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| subnet | name, <br/>ip_ranges, <br/>ipspace, <br/>broadcast_domain, <br/>subnet, <br/>gateway |







## ontap / svm

Manage NetApp ONTAP SVMs (vservers)  
  
Note : This role supports multi / looping





### Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [clean](#svm--clean) |  |
| [create](#svm--create) |  |
| [delete](#svm--delete) |  |



### svm / clean

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Search svm  | netapp.ontap | na_ontap_rest_info |  |  |
| Role - ontap/svm/delete |  | block |  |  |


**Variables**

| Variable | Properties |
| :------- | :--------- |



### svm / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Create Svm  | netapp.ontap | na_ontap_svm |  | ipspace, svm |
| Get aggr list | netapp.ontap | na_ontap_rest_info |  |  |
| Set aggregate list  | netapp.ontap | na_ontap_svm |  | aggr_info, svm |
| Move and rename root volume  | netapp.ontap | na_ontap_volume |  | svm |
| Set SVM Options  | netapp.ontap | na_ontap_svm_options | x | svm |
| Create Lifs  |  | include_tasks | x | svm |
| create default route  | netapp.ontap | na_ontap_net_routes | x | svm |
| Get vserver uuid | netapp.ontap | na_ontap_restit |  |  |
| Set other svm parameters (using restit)  | netapp.ontap | na_ontap_restit |  | svm_info |
| Set other svm parameters (using rest_cli)  | netapp.ontap | na_ontap_rest_cli |  |  |
| Create dns  |  | include_tasks |  |  |
| Enable cifs  |  | include_tasks |  |  |
| Create Domain Tunnel  | netapp.ontap | na_ontap_domain_tunnel |  | svm |
| Set vscan  | netapp.ontap | na_ontap_vscan |  | svm |
| Enable nfs  |  | include_tasks |  |  |
| Enable iscsi  |  | include_tasks |  |  |
| Create volumes on  |  | include_tasks | x | svm |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| aggr_info | ontap_info |
| ipspace | name |
| svm | name, <br/>allowed_protocols, <br/>snapshot_policy, <br/>language, <br/>comment, <br/>max_volumes, <br/>subtype, <br/>root_volume, <br/>options, <br/>lifs, <br/>vscan_enable, <br/>volumes |
| svm_info | response |



### svm / delete

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Clean svm  |  | include_tasks |  |  |
| Delete svm  | netapp.ontap | na_ontap_svm |  | svm |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| svm | name |







## ontap / unix_group

Manage NetApp ONTAP Unix Groups  
  






### Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [create](#unix_group--create) |  |



### unix_group / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Create Unix Group  | netapp.ontap | na_ontap_unix_group |  | svm, unix_group |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| svm | name |
| unix_group | name, <br/>users, <br/>id |







## ontap / unix_user

Manage NetApp ONTAP Unix Users  
  






### Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [create](#unix_user--create) |  |



### unix_user / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Create Unix User  | netapp.ontap | na_ontap_unix_user |  | svm, unix_user |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| svm | name |
| unix_user | name, <br/>full_name, <br/>group_id, <br/>id |







## ontap / user

Manage NetApp ONTAP Users  
  






### Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [create](#user--create) |  |



### user / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Create user  | netapp.ontap | na_ontap_user |  | svm, user |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| svm | name |
| user | name, <br/>role_name, <br/>authentication_password, <br/>application_strs, <br/>authentication_method |







## ontap / vlan

Manage NetApp ONTAP VLANs  
  
Note : This role supports multi / looping





### Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [create](#vlan--create) |  |



### vlan / create

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







## ontap / volume

Manage NetApp ONTAP volumes  
  
Note : This role supports multi / looping





### Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [create](#volume--create) |  |
| [create_dp](#volume--create_dp) |  |
| [decom](#volume--decom) |  |
| [delete](#volume--delete) |  |
| [delete_lock](#volume--delete_lock) |  |
| [modify](#volume--modify) |  |
| [move](#volume--move) |  |
| [offline](#volume--offline) |  |
| [online](#volume--online) |  |
| [rename](#volume--rename) |  |
| [resize](#volume--resize) |  |



### volume / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Find best aggregate  |  | get_best_aggregate |  | svm, volume |
| Create volume  | netapp.ontap | na_ontap_volume |  | svm, volume |
| Set efficiency  | netapp.ontap | na_ontap_volume_efficiency |  | svm, volume |
| Set compression type  | netapp.ontap | na_ontap_rest_cli |  |  |
| Set efficiency schedule  | netapp.ontap | na_ontap_rest_cli |  |  |
| Set volume autosize  | netapp.ontap | na_ontap_volume_autosize |  | svm, volume |
| Set volume snapshot autodelete  | netapp.ontap | na_ontap_rest_cli |  |  |
| Set space-mgmt-try-first  | netapp.ontap | na_ontap_rest_cli |  |  |
| Get volume uuid  | netapp.ontap | na_ontap_restit |  |  |
| Set anti-ransomware state  | netapp.ontap | na_ontap_restit |  | volume_info |
| Set read-alloc  | netapp.ontap | na_ontap_rest_cli |  |  |
| Set fractional-reserve  | netapp.ontap | na_ontap_rest_cli |  |  |
| Set atime-update  | netapp.ontap | na_ontap_rest_cli |  |  |
| Create qtrees  |  | include_tasks | x | volume |
| Create luns  |  | include_tasks | x | volume |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| svm | name |
| volume | name, <br/>size, <br/>aggregate_include_node_regex, <br/>activity_tracking, <br/>analytics, <br/>auto_remap_luns, <br/>aggregate, <br/>size_unit, <br/>space_guarantee, <br/>percent_snapshot_space, <br/>wait_for_completion, <br/>junction_path, <br/>language, <br/>comment, <br/>type, <br/>atime_update, <br/>compression, <br/>encrypt, <br/>group_id, <br/>inline_compression, <br/>size_change_threshold, <br/>unix_permissions, <br/>user_id, <br/>security_style, <br/>snaplock, <br/>logical_space_reporting, <br/>logical_space_enforcement, <br/>efficiency_policy, <br/>export_policy, <br/>snapshot_policy, <br/>tiering_policy, <br/>qos_policy_group, <br/>qos_adaptive_policy_group, <br/>volume_efficiency, <br/>volume_autosize, <br/>qtrees, <br/>luns |
| volume_info | response |



### volume / create_dp

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Find best aggregate  |  | get_best_aggregate |  | svm, volume |
| Create dp volume  | netapp.ontap | na_ontap_volume |  | svm, volume |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| svm | name |
| volume | name, <br/>size, <br/>aggregate_include_node_regex, <br/>aggregate, <br/>activity_tracking, <br/>analytics, <br/>size_unit, <br/>space_guarantee, <br/>percent_snapshot_space, <br/>wait_for_completion, <br/>language, <br/>comment, <br/>atime_update, <br/>compression, <br/>encrypt, <br/>inline_compression, <br/>size_change_threshold, <br/>snaplock, <br/>efficiency_policy, <br/>export_policy, <br/>snapshot_policy, <br/>tiering_policy, <br/>qos_policy_group, <br/>qos_adaptive_policy_group |



### volume / decom

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Unmount volume  | netapp.ontap | na_ontap_volume |  | svm, volume |
| Set comment with timestamp on volume  | netapp.ontap | na_ontap_volume |  | , svm, volume |
| Rename volume  | netapp.ontap | na_ontap_volume |  | svm, volume |


**Variables**

| Variable | Properties |
| :------- | :--------- |
|  |  |
| svm | name |
| volume | name |



### volume / delete

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Collect cifs shares for volume  | netapp.ontap | na_ontap_rest_info |  |  |
| Remove cifs shares for volume  |  | include_tasks | x | cifs_share_info |
| Delete volume  | netapp.ontap | na_ontap_volume |  | svm, volume |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| cifs_share_info | ontap_info |
| svm | name |
| volume | name |



### volume / delete_lock

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Get locks on volume  | netapp.ontap | na_ontap_restit |  |  |
| Delete locks on volume  | netapp.ontap | na_ontap_restit | x | lock, locks_info |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| lock | uuid |
| locks_info | response |



### volume / modify

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| modify volume  | netapp.ontap | na_ontap_volume |  | svm, volume |
| Set efficiency  | netapp.ontap | na_ontap_volume_efficiency |  | svm, volume |
| Set compression type  | netapp.ontap | na_ontap_rest_cli |  |  |
| Set efficiency schedule  | netapp.ontap | na_ontap_rest_cli |  |  |
| Set volume autosize  | netapp.ontap | na_ontap_volume_autosize |  | svm, volume |
| Set volume snapshot autodelete  | netapp.ontap | na_ontap_rest_cli |  |  |
| Set space-mgmt-try-first  | netapp.ontap | na_ontap_rest_cli |  |  |
| Get volume uuid  | netapp.ontap | na_ontap_restit |  |  |
| Set anti-ransomware state  | netapp.ontap | na_ontap_restit |  | volume_info |
| Set read-alloc  | netapp.ontap | na_ontap_rest_cli |  |  |
| Set fractional-reserve  | netapp.ontap | na_ontap_rest_cli |  |  |
| Set atime-update  | netapp.ontap | na_ontap_rest_cli |  |  |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| svm | name |
| volume | name, <br/>type, <br/>is_online, <br/>activity_tracking, <br/>analytics, <br/>auto_remap_luns, <br/>junction_path, <br/>language, <br/>comment, <br/>atime_update, <br/>compression, <br/>encrypt, <br/>group_id, <br/>inline_compression, <br/>size_change_threshold, <br/>unix_permissions, <br/>user_id, <br/>security_style, <br/>snaplock, <br/>logical_space_reporting, <br/>logical_space_enforcement, <br/>efficiency_policy, <br/>export_policy, <br/>snapshot_policy, <br/>tiering_policy, <br/>qos_policy_group, <br/>qos_adaptive_policy_group, <br/>volume_efficiency, <br/>volume_autosize |
| volume_info | response |



### volume / move

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Find best aggregate  |  | get_best_aggregate |  | svm, volume |
| Move volume  | netapp.ontap | na_ontap_volume |  | svm, volume |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| svm | name |
| volume | name, <br/>size, <br/>aggregate_include_node_regex, <br/>aggregate |



### volume / offline

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Offline volume  | netapp.ontap | na_ontap_volume |  | svm, volume |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| svm | name |
| volume | name |



### volume / online

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Online volume  | netapp.ontap | na_ontap_volume |  | svm, volume |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| svm | name |
| volume | name |



### volume / rename

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Rename volume  | netapp.ontap | na_ontap_volume |  | svm, volume |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| svm | name |
| volume | old_name, <br/>name |



### volume / resize

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Resize volume  | netapp.ontap | na_ontap_volume |  | svm, volume |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| svm | name |
| volume | name, <br/>size, <br/>size_unit |







## ontap / vscan_scanner_pool

Manage NetApp ONTAP Vscan Scanner Pools  
  






### Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [create](#vscan_scanner_pool--create) |  |



### vscan_scanner_pool / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Create Vscan Scanner Pool  | netapp.ontap | na_ontap_scanner_pool |  | svm, vscan_scanner_pool |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| svm | name |
| vscan_scanner_pool | scanner_pool, <br/>scanner_policy, <br/>privileged_users, <br/>hostnames |







## ontap / vserver_peer

Manage NetApp ONTAP Vserver Peers  
  






### Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [create](#vserver_peer--create) |  |



### vserver_peer / create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Create vserver peering  | netapp.ontap | na_ontap_vserver_peer |  | vserver_peer |
| wait for vserver peering to be established |  | pause |  |  |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| vserver_peer |  |








