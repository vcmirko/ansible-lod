# awx / job 
Manages AWX job tasks  
  






## Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [concurrent_launch](#job--concurrent_launch) |  |



## job / concurrent_launch

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Process the awx_concurrent object |  | awx_concurrent_loop |  | vars_external |
| Get awx_concurrent result |  | set_fact |  |  |
| Launch Job Template for Each Item Concurrently | awx.awx | job_launch | x | awx_concurrent_items, awx_hostname, awx_password, awx_username |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| awx_concurrent_items |  |
| awx_hostname |  |
| awx_password |  |
| awx_username |  |
| vars_external |  |




