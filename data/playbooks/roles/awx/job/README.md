# awx / job 
Manages AWX job tasks  
  





## Custom Modules

| Module | Description | Version History |
| :----- | :---------- | :-------------- |
| awx_concurrent_loop.py | Will convert the input to a format that can be used in a loop to create multiple jobs in AWX | 2025-02-03 - Mirko Van Colen - Initial version |



## Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [concurrent_launch](#job--concurrent_launch) |  |




## job / concurrent_launch


| Task |
| :--- |
| Process the awx_concurrent object |
| Get awx_concurrent result |
| Launch Job Template for Each Item Concurrently |




