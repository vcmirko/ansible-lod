# Templates

These are used for the 3 python scripts :

- create_role.py
- check_roles.py
- document_roles.py

## Create Role
An interactive script that create a new role.  
Rule the check_roles and documenent_roles script after this, to fix/complete missing parts

## Check Roles
Will flag errors and fix issues, like missing files.
Multi files or missing meta and main files will be created.

## Document Roles
Will generate README.md files.  These are overwritten.  It uses the `galaxy.yml` from the collection root path and the `main.yml` in each `meta` folder of each role.

Each role task (`create`, `delete`, ...) must with extension `.yml` and must have a block with starting name.  The name will be of the format "Role - collection/role/task".  And the block will then contain tasks with names.  

The script will flag missing parts in the files.  
When exposing variables in a name of a task, wrap it with square brackets.  These will be removed in the documentation.