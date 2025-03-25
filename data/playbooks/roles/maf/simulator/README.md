# maf / simulator 
Deploy ontap simulator  
  






## Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [cluster_config](#simulator--cluster_config) |  |
| [cluster_init](#simulator--cluster_init) |  |
| [cluster_init2](#simulator--cluster_init2) |  |
| [deploy_sim](#simulator--deploy_sim) |  |
| [destroy_sim](#simulator--destroy_sim) |  |
| [init_sim](#simulator--init_sim) |  |



## simulator / cluster_config

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Wait for cluster to stabilize |  | wait_for |  |  |
| set timezone | netapp.ontap | na_ontap_rest_cli |  | netapp_hostname, netapp_password, netapp_username |
| get nodes | netapp.ontap | na_ontap_rest_info |  | netapp_hostname, netapp_password, netapp_username |
| Unlock User diag | netapp.ontap | na_ontap_user |  | netapp_hostname, netapp_password, netapp_username |
| Add licenses | netapp.ontap | na_ontap_license |  | cluster_license_codes, netapp_hostname, netapp_password, netapp_username |
| Assign disks | netapp.ontap | na_ontap_disks |  | netapp_hostname, netapp_password, netapp_username, nodes |
| create aggr1 | netapp.ontap | na_ontap_aggregate |  | netapp_hostname, netapp_password, netapp_username, nodes |
| create DNS on cluster | netapp.ontap | na_ontap_dns |  | cluster_dns_domain, cluster_dns_server, cluster_name, netapp_hostname, netapp_password, netapp_username |
| create Broadcast domains | netapp.ontap | na_ontap_broadcast_domain | x | cluster_vlans, netapp_hostname, netapp_password, netapp_username |
| create VLANs | netapp.ontap | na_ontap_net_vlan | x | cluster_vlan_port, cluster_vlans, netapp_hostname, netapp_password, netapp_username, nodes |
| add vlans to broadcast domain | netapp.ontap | na_ontap_broadcast_domain | x | cluster_vlans, netapp_hostname, netapp_password, netapp_username |
| Create inter cluster lif |  | na_ontap_interface |  | cluster_intercluster_port, cluster_netmask, netapp_hostname, netapp_password, netapp_username, nodes |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| cluster_dns_domain |  |
| cluster_dns_server |  |
| cluster_intercluster_port |  |
| cluster_license_codes |  |
| cluster_name |  |
| cluster_netmask |  |
| cluster_vlan_port |  |
| cluster_vlans |  |
| netapp_hostname |  |
| netapp_password |  |
| netapp_username |  |
| nodes |  |



## simulator / cluster_init

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Wait for {{ simulator_node_setup_delay }} seconds for Startup to Complete |  | wait_for |  | simulator_node_setup_delay |
| Complete Node Setup | community.vmware | vmware_guest_sendkey | x | cluster, item, vcenter_host, vcenter_password, vcenter_username |
| Run cluster setup on {{ cluster.name }} |  | block |  |  |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| cluster | name |
| item |  |
| simulator_node_setup_delay |  |
| vcenter_host |  |
| vcenter_password |  |
| vcenter_username |  |



## simulator / cluster_init2

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Run cluster setup on {{ cluster.name }} |  | block |  |  |


**Variables**

| Variable | Properties |
| :------- | :--------- |



## simulator / deploy_sim

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Deploy ovf file: {{ simulator_ovf_file }} | community.vmware | vmware_deploy_ovf |  | playbook_dir, simulator, simulator_ovf_file, simulator_ovf_path, simulator_vm_datastore, simulator_vm_disk_provisioning, simulator_vm_name, vcenter_cluster, vcenter_host, vcenter_password, vcenter_username |
| Adjust VM Sizing | community.vmware | vmware_guest |  | simulator_vm_name, vcenter_host, vcenter_password, vcenter_username |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| playbook_dir |  |
| simulator | vcenter_datacenter |
| simulator_ovf_file |  |
| simulator_ovf_path |  |
| simulator_vm_datastore |  |
| simulator_vm_disk_provisioning |  |
| simulator_vm_name |  |
| vcenter_cluster |  |
| vcenter_host |  |
| vcenter_password |  |
| vcenter_username |  |



## simulator / destroy_sim

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Destroy vm {{ cluster_name}} |  | vmware_guest |  | cluster_name, vcenter_host, vcenter_password, vcenter_username |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| cluster_name |  |
| vcenter_host |  |
| vcenter_password |  |
| vcenter_username |  |



## simulator / init_sim

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Set authentication |  | set_fact |  |  |
| Start VM | community.vmware | vmware_guest |  | simulator_vm_name, vcenter_host, vcenter_password, vcenter_username |
| Wait for 10 seconds |  | wait_for |  |  |
| Press Space to interrupt autoboot | community.vmware | vmware_guest_sendkey | x | simulator_vm_name, vcenter_host, vcenter_password, vcenter_username |
| configure loader variable via sendkeys | community.vmware | vmware_guest_sendkey | x | simulator_vm_name, vcenter_host, vcenter_password, vcenter_username |
| verbose console | community.vmware | vmware_guest_sendkey | x | simulator_vm_name, vcenter_host, vcenter_password, vcenter_username |
| clear nvram_sysid |  | set_fact |  |  |
| set extra bootargs | community.vmware | vmware_guest_sendkey | x | simulator_bootargs, simulator_vm_name, vcenter_host, vcenter_password, vcenter_username |
| boot_ontap | community.vmware | vmware_guest_sendkey | x | item, simulator_vm_name, vcenter_host, vcenter_password, vcenter_username |
| Wait for VMware tools to become available | community.vmware | vmware_guest_tools_wait |  | simulator_vm_name, vcenter_host, vcenter_password, vcenter_username |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| item |  |
| simulator_bootargs |  |
| simulator_vm_name |  |
| vcenter_host |  |
| vcenter_password |  |
| vcenter_username |  |




