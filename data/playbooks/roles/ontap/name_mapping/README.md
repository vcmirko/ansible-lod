# ontap / name_mapping

This role is used to create name mappings on an SVM.

## tasks

- create : create name mappings on an SVM (required credentials : ontap)

## Input

- cluster.management_ip
- svm.name
- name_mapping.direction
- name_mapping.index
- name_mapping.pattern
- name_mapping.replacement
- name_mapping.client_match
