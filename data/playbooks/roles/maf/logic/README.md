# maf / logic 
-- Missing description --  
  






## Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [bypass](#logic--bypass) |  |
| [svm_create](#logic--svm_create) |  |
| [svm_delete](#logic--svm_delete) |  |
| [svm_dr](#logic--svm_dr) |  |



## logic / bypass

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Running logic bypass |  | bypass |  | vars_external |
| Register logic result |  | set_fact |  |  |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| vars_external |  |



## logic / svm_create

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Logic - svm_create |  | svm_create |  | vars_external |
| Register logic result |  | set_fact |  |  |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| vars_external |  |



## logic / svm_delete

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Logic - svm_delete |  | svm_delete |  | aiqum_host, aiqum_password, aiqum_username, vars_external |
| Register logic result |  | set_fact |  |  |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| aiqum_host |  |
| aiqum_password |  |
| aiqum_username |  |
| vars_external |  |



## logic / svm_dr

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Logic - svm_dr |  | svm_dr |  | vars_external |
| Register logic result |  | set_fact |  |  |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| vars_external |  |




