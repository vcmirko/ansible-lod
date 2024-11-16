# ontap / security_certificate

This role is used to renew a security certificate on an SVM.

## tasks

- renew : renew a security certificate on an SVM (required credentials : ontap)

## Input

- cluster.management_ip
- svm.name
- security_certificate.expiry_days : the number of days before the certificate expires to renew it
- security_certificate.days : the number of days the new certificate is valid
