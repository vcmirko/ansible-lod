# api_certificates

To use certificates to connect to ONTAP clusters, client certificates (private key and public key) should be generated, stored and passed.  
This MAF frameworks contains a role (`ontap/cluster/create_api_user`) and sample playbook for this (`test_create_api_user_with_inventory`).
  
The certificates are stored in this folder by default.  
Use the `var/defaults.yml` to configure the api certificate behaviour.