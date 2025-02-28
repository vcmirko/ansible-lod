# infoblox / ip_management 
Manage IP addresses in Infoblox  
  






## Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [register](#ip_management--register) |  |
| [request](#ip_management--request) |  |
| [unregister](#ip_management--unregister) |  |



## ip_management / register

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Register DNS address with Infoblox A-record | infoblox.nios_modules | nios_a_record |  | input_dns_domain, new_free_ip_addr, new_short_hostname |
| Fail the play if Infoblox is not reachable | ansible.builtin | fail |  |  |
| Register DNS address with Infoblox PTR-record | infoblox.nios_modules | nios_ptr_record |  | input_dns_domain, new_free_ip_addr, new_short_hostname |
| Fail the play if error occured during PTR registration | ansible.builtin | fail |  |  |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| input_dns_domain |  |
| new_free_ip_addr |  |
| new_short_hostname |  |



## ip_management / request

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Find Ip Address if non is given |  | block |  |  |
| Find pre-registered ip |  | block |  |  |
| Retrieve net info from DCHP for given network {{ infoblox.network }} (Infoblox) | ansible.builtin | set_fact |  |  |
| Validating data returned by nfoblox for DNS servers, domain or gateway information | ansible.builtin | fail |  |  |
| Setting basic network facts - NDS server list, domain and gateway from data provided in the Infoblox response | ansible.builtin | set_fact |  |  |
| Make dict from result | ansible.builtin | set_fact |  |  |


**Variables**

| Variable | Properties |
| :------- | :--------- |



## ip_management / unregister

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Unregister IP address from Infoblox A-records | infoblox.nios_modules | nios_a_record |  | input_dns_domain, ip_addr, new_short_hostname |
| Fail the play if Infoblox is not reachable | ansible.builtin | fail |  |  |
| Unregister DNS address with Infoblox PTR-record | infoblox.nios_modules | nios_ptr_record |  | input_dns_domain, ip_addr, new_short_hostname |
| Fail the play error occured during PTR unregistration | ansible.builtin | fail |  |  |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| input_dns_domain |  |
| ip_addr |  |
| new_short_hostname |  |




