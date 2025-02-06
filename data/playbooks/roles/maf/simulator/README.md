# maf / simulator 
Deploy, destroy ONTAP simulator  
  






## Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [cluster_config](#simulator--cluster_config) |  |
| [cluster_init](#simulator--cluster_init) |  |
| [deploy_sim](#simulator--deploy_sim) |  |
| [destroy_sim](#simulator--destroy_sim) |  |
| [init_sim](#simulator--init_sim) |  |




## simulator / cluster_config


| Task |
| :--- |
| Wait for cluster to stabilize |
| set timezone |
| get nodes |
| Unlock User diag |
| Add licenses |
| Assign disks |
| create aggr1 |
| create DNS on cluster |
| create Broadcast domains |
| create VLANs |
| add vlans to broadcast domain |
| Create inter cluster lif |



## simulator / cluster_init


| Task |
| :--- |
| Wait for {{ simulator_node_setup_delay }} seconds for Startup to Complete |
| Complete Node Setup |
| Run cluster setup on {{ cluster.name }} |



## simulator / deploy_sim


| Task |
| :--- |
| Deploy ovf file: {{ simulator_ovf_file }} |
| Adjust VM Sizing |



## simulator / destroy_sim


| Task |
| :--- |
| Destroy vm {{ cluster_name}} |



## simulator / init_sim


| Task |
| :--- |
| Set authentication |
| Start VM |
| Wait for 10 seconds |
| Press Space to interrupt autoboot |
| configure loader variable via sendkeys |
| verbose console |
| clear nvram_sysid |
| set extra bootargs |
| boot_ontap |
| Wait for VMware tools to become available |




