# cyberark / pam 
Manages CyberArk PAM tasks  
  






## Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [account_add](#pam--account_add) |  |
| [account_delete](#pam--account_delete) |  |
| [account_reconcile](#pam--account_reconcile) |  |
| [authenticate](#pam--authenticate) |  |



## pam / account_add

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Add new account |  | no_log |  |  |


**Variables**

| Variable | Properties |
| :------- | :--------- |



## pam / account_delete

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Remove existing account |  | uri |  | pam, pam_account |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| pam | hostname |
| pam_account | id |



## pam / account_reconcile

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Reconcile existing account |  | no_log |  |  |


**Variables**

| Variable | Properties |
| :------- | :--------- |



## pam / authenticate

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| Authenticate to CyberArk PAM |  | uri |  | pam |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| pam | hostname |




