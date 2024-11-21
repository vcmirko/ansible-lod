# Tasks Summary

## create.yml
This file supports the following properties:

### cluster
| Property       | Description                                |
|----------------|--------------------------------------------|
| **name**       | The name of the cluster.                   |
| **management_ip** | The ip or fqdn of the cluster. |

### svm
| Property       | Description                                |
|----------------|--------------------------------------------|
| **name**       | The name of the SVM.                       |
| **services**   | The services enabled on the SVM.           |
| **subtype**    | The subtype of the SVM.                    |

### cifs
| Property                   | Description                                |
|----------------------------|--------------------------------------------|
| **name**                   | The name of the CIFS server.               |
| **domain**                 | The domain for the CIFS server.            |
| **ou**                     | The organizational unit for the CIFS server.|
| **session_security**       | The session security for the CIFS server.  |
| **smb_encryption**         | The SMB encryption for the CIFS server.    |
| **smb_signing**            | The SMB signing for the CIFS server.       |
| **try_ldap_channel_binding**| Whether to try LDAP channel binding.      |
| **restrict_anonymous**     | Whether to restrict anonymous access.      |
| **lm_compatibility_level** | The LM compatibility level.                |
| **ldap_referral_enabled**  | Whether LDAP referral is enabled.          |
| **kdc_encryption**         | The KDC encryption type.                   |
| **is_multichannel_enabled**| Whether multichannel is enabled.           |
| **encrypt_dc_connection**  | Whether to encrypt DC connection.          |
| **default_site**           | The default site.                          |
| **aes_netlogon_enabled**   | Whether AES netlogon is enabled.           |
| **is_advertise_dfs_enabled**| Whether to advertise DFS.                 |
| **is_nbns_enabled**        | Whether NBNS is enabled.                   |
| **privileges**             | A list of CIFS privileges.                 |
| **administrators**         | A list of CIFS administrators.             |

### ad_username
| Property       | Description                                |
|----------------|--------------------------------------------|
| **The Active Directory username**|                          |

### ad_password
| Property       | Description                                |
|----------------|--------------------------------------------|
| **The Active Directory password**|                          |

## delete.yml
This file supports the following properties:

### cluster
| Property       | Description                                |
|----------------|--------------------------------------------|
| **name**       | The name of the cluster.                   |
| **management_ip** | The ip or fqdn of the cluster. |

### svm
| Property       | Description                                |
|----------------|--------------------------------------------|
| **name**       | The name of the SVM.                       |

### cifs
| Property                   | Description                                |
|----------------------------|--------------------------------------------|
| **name**                   | The name of the CIFS server.               |

### ad_username
| Property       | Description                                |
|----------------|--------------------------------------------|
| **The Active Directory username**|                          |

### ad_password
| Property       | Description                                |
|----------------|--------------------------------------------|
| **The Active Directory password**|                          |

## stop.yml
This file supports the following properties:

### cluster
| Property       | Description                                |
|----------------|--------------------------------------------|
| **name**       | The name of the cluster.                   |
| **management_ip** | The ip or fqdn of the cluster. |

### svm
| Property       | Description                                |
|----------------|--------------------------------------------|
| **name**       | The name of the SVM.                       |

### cifs
| Property                   | Description                                |
|----------------------------|--------------------------------------------|
| **name**                   | The name of the CIFS server.               |
