# ontap / cluster 
Manage NetApp ONTAP Cluster  
  






## Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [create_api_user](#cluster--create_api_user) |  |
| [example_report](#cluster--example_report) |  |
| [test_api_user](#cluster--test_api_user) |  |



## cluster / create_api_user

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| check if the certificate exists |  | stat |  | cluster_api_cert_filepath |
| get expiry days from certificate |  | set_fact |  |  |
| renew the certificate if the expiry date is due to renewal |  | block |  |  |
| create the api user | netapp.ontap | na_ontap_user |  | cluster_api_role, cluster_api_username, netapp_hostname, netapp_password, netapp_username |
| test the api user | netapp.ontap | na_ontap_rest_info |  | cluster_api_cert_filepath, cluster_api_key_filepath, netapp_hostname |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| cluster_api_cert_filepath |  |
| cluster_api_key_filepath |  |
| cluster_api_role |  |
| cluster_api_username |  |
| netapp_hostname |  |
| netapp_password |  |
| netapp_username |  |



## cluster / example_report

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| get cluster info | netapp.ontap | na_ontap_rest_info |  |  |
| Print cluster info |  | debug |  |  |


**Variables**

| Variable | Properties |
| :------- | :--------- |



## cluster / test_api_user

| Task | Collection | Module | Looped | Variables |
| :--- | :--------- | :----- | :----- | :-------- |
| test the api user | netapp.ontap | na_ontap_rest_info |  | cluster_api_cert_filepath, cluster_api_key_filepath, netapp_hostname |


**Variables**

| Variable | Properties |
| :------- | :--------- |
| cluster_api_cert_filepath |  |
| cluster_api_key_filepath |  |
| netapp_hostname |  |




