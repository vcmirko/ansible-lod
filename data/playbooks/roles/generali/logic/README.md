# generali / logic 
Manages the logic of the Generali, like naming conventions, environment placing, etc.  
  





## Custom Modules

| Module | Description | Version History |
| :----- | :---------- | :-------------- |
| uc01_create_volume.py | The custom logic used to create a volume<br><br>It's setting the SVM & volume names based on the primary SVM & volume names<br>and then removing the environments that are not needed based on the service level & volume_dr<br><br>Setting the export policy name based on the volume style<br>Creating a CIFS share if the volume style is SMB or MIX<br>Settings proper ACL's on the CIFS share<br>Add template to the CIFS share to apply properties from the templates_generali.yaml file<br>-> to add the CIFS share properties like access_based_enumeration, oplocks, ...<br>-> Used to be passed by vrealize, but now it's hardcoded in the templates_generali.yaml file<br>-> Old values were zapi based and not working for rest api<br>When is_ivz is True, no export policy rules are set, this is for Germany only and has its own rules<br>Adding junction path to the volume<br>Adding adaptive QoS policy to the volume<br>Disabling autosize if needed<br>Setting snapshot policy's<br>Setting snapmirror policy's and schedules<br>Adpe has a different snapmirror policy and schedule (fixed VP_30 and ADPE schedule) | 2025-02-03 - Mirko Van Colen - Initial version |
| uc02_delete_volume.py | The custom logic used to delete a volume<br><br>It's setting the SVM & volume names based on the primary SVM & volume names<br>and then removing the environments that are not needed based on the service level<br><br>It's also making date-based new volume names for the rename action<br>It's also removing the export policy name if it's the default one, to avoid deleting it | 2025-02-03 - Mirko Van Colen - Initial version |
| uc03_resize_volume.py | The custom logic used to resize a volume<br><br>It's setting the SVM & volume names based on the primary SVM & volume names<br>and then removing the environments that are not needed based on the service level<br><br>No further logic is needed | 2025-02-03 - Mirko Van Colen - Initial version |
| uc05_create_qtree.py | The custom logic used to create a qtree<br><br>It's deciding whether to create a quota and / or cifs share based on the metadata<br>It's setting the quota target based on the volume & qtree name<br>It's setting the SVM & volume names based on the primary SVM & volume names<br>It's removing the environments that are not needed based on the service level<br>Quota is only set on primary<br>Shares are synced to all environments | 2025-02-03 - Mirko Van Colen - Initial version |
| uc06_resize_quota.py | The custom logic used to resize a quota<br><br>It's only purpose is setting the quota target based on the volume & qtree name | 2025-02-03 - Mirko Van Colen - Initial version |
| uc17_create_export.py | The custom logic used to delete an export from a volume<br><br>It's 100% the same as delete export<br>It's simply setting volume & svm names based on the primary volume & svm names<br>and then removing the environments that are not needed based on the service level | 2025-02-03 - Mirko Van Colen - Initial version |
| uc18_delete_export.py | The custom logic used to delete an export from a volume<br><br>It's 100% the same as create export<br>It's simply setting volume & svm names based on the primary volume & svm names<br>and then removing the environments that are not needed based on the service level | 2025-02-03 - Mirko Van Colen - Initial version |



## Role actions/qtasks

| Subrole | Description |
| :------ | :---------- |
| [uc01_create_volume](#logic--uc01_create_volume) |  |
| [uc02_delete_volume](#logic--uc02_delete_volume) |  |
| [uc03_resize_volume](#logic--uc03_resize_volume) |  |
| [uc05_create_qtree](#logic--uc05_create_qtree) |  |
| [uc06_resize_quota](#logic--uc06_resize_quota) |  |
| [uc17_create_export](#logic--uc17_create_export) |  |
| [uc18_delete_export](#logic--uc18_delete_export) |  |




## logic / uc01_create_volume


| Task |
| :--- |
| Get Primary Cluster Name |
| Get Backup Local Cluster Name |
| Get Backup Remote Cluster Name |
| Get ADPE Cluster Name |
| Apply vrealize input to vars_external |
| Logic - UC01 Create Volume |
| Register logic result |



## logic / uc02_delete_volume


| Task |
| :--- |
| Get Primary Cluster Name |
| Get Backup Local Cluster Name |
| Get Backup Remote Cluster Name |
| Get ADPE Cluster Name |
| Apply vrealize input to vars_external |
| Logic - UC02 Delete Volume |
| Register logic result |



## logic / uc03_resize_volume


| Task |
| :--- |
| Apply vrealize input to vars_external |
| Logic - uc03 Resize Volume |
| Register logic result |



## logic / uc05_create_qtree


| Task |
| :--- |
| Get Primary Cluster Name |
| Get Backup Local Cluster Name |
| Get Backup Remote Cluster Name |
| Get ADPE Cluster Name |
| Apply vrealize input to vars_external |
| Logic - uc05 create qtree |
| Register logic result |



## logic / uc06_resize_quota


| Task |
| :--- |
| Apply vrealize input to vars_external |
| Logic - uc06 resize quota |
| Register logic result |



## logic / uc17_create_export


| Task |
| :--- |
| Apply vrealize input to vars_external |
| Logic - uc17 create export |
| Register logic result |



## logic / uc18_delete_export


| Task |
| :--- |
| Apply vrealize input to vars_external |
| Logic - uc18 delete export |
| Register logic result |




