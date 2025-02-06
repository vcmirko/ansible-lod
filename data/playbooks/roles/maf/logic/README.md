# maf / logic 
Some sample logic for MAF  
  





## Custom Modules

| Module | Description | Version History |
| :----- | :---------- | :-------------- |
| bypass.py | This script is a blank template for custom logic, currently it does nothing and bypasses vars_external to the output | 2025-02-03 - Mirko Van Colen - Initial version |
| svm_create.py | This script is the custom logic used to create a SVM and volumes<br><br>Adding a few lifs, setting volume junction paths and setting the template | 2025-02-03 - Mirko Van Colen - Initial version |
| svm_delete.py | This script is the custom logic used to delete an svm<br><br>Deleting an svm, requires having a list of all clusters (management_ip & name) that can have a snapmirror relationship<br>This script will connect to AIQUM and get all cluster information and inject it into the vars_external dict | 2025-02-03 - Mirko Van Colen - Initial version |
| svm_dr.py | This script is the custom logic for an svm dr demo<br><br>It will complete the vars_external dict with snapmirror relationship information<br>Junctionpaths, naming conventions, etc | 2025-02-03 - Mirko Van Colen - Initial version |



## Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [bypass](#logic--bypass) |  |
| [svm_create](#logic--svm_create) |  |
| [svm_delete](#logic--svm_delete) |  |
| [svm_dr](#logic--svm_dr) |  |




## logic / bypass


| Task |
| :--- |
| Running logic bypass |
| Register logic result |



## logic / svm_create


| Task |
| :--- |
| Logic - svm_create |
| Register logic result |



## logic / svm_delete


| Task |
| :--- |
| Logic - svm_delete |
| Register logic result |



## logic / svm_dr


| Task |
| :--- |
| Logic - svm_dr |
| Register logic result |




