# aiqum / management 
AIQUM management, register, rediscover, ...  
  






## Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [rediscover](#management--rediscover) |  |
| [register](#management--register) |  |
| [unregister](#management--unregister) |  |



## management / rediscover

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Get CLUSTER in Aiqum |  | uri |  | aiq_hostname, aiq_password, aiq_username, cluster_name |
| Rediscover Aiqum for CLUSTER |  | uri |  | aiq_hostname, aiq_password, aiq_username, cluster_obj |
| Wait for operation |  | uri |  | aiq_hostname, aiq_password, aiq_username, rediscover_operation |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| aiq_hostname |  |
| aiq_password |  |
| aiq_username |  |
| cluster_name |  |
| cluster_obj | json |
| rediscover_operation | json |



## management / register

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Get CLUSTER in Aiqum |  | uri |  | aiq_hostname, aiq_password, aiq_username, cluster_name |
| Register CLUSTER in Aiqum |  | block |  |  |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| aiq_hostname |  |
| aiq_password |  |
| aiq_username |  |
| cluster_name |  |



## management / unregister

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Get CLUSTER in Aiqum |  | uri |  | aiq_hostname, aiq_password, aiq_username, cluster_name |
| Delete CLUSTER in Aiqum |  | uri |  | aiq_hostname, aiq_password, aiq_username, cluster_obj |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| aiq_hostname |  |
| aiq_password |  |
| aiq_username |  |
| cluster_name |  |
| cluster_obj | json |




