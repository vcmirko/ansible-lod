# infoblox / ip_management 
Manage IP addresses in Infoblox  
  






## Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [register](#ip_management--register) |  |
| [request](#ip_management--request) |  |
| [unregister](#ip_management--unregister) |  |




## ip_management / register


| Task |
| :--- |
| Register DNS address with Infoblox A-record |
| Fail the play if Infoblox is not reachable |
| Register DNS address with Infoblox PTR-record |
| Fail the play if error occured during PTR registration |



## ip_management / request


| Task |
| :--- |
| Find Ip Address if non is given |
| Find pre-registered ip |
| Retrieve net info from DCHP for given network {{ infoblox.network }} (Infoblox) |
| Validating data returned by nfoblox for DNS servers, domain or gateway information |
| Setting basic network facts - NDS server list, domain and gateway from data provided in the Infoblox response |
| Make dict from result |



## ip_management / unregister


| Task |
| :--- |
| Unregister IP address from Infoblox A-records |
| Fail the play if Infoblox is not reachable |
| Unregister DNS address with Infoblox PTR-record |
| Fail the play error occured during PTR unregistration |




