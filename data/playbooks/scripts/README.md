# Scripts

This scripts folder contains 3 python scripts :

- create_role : Will interactively help you to create a new role
- check_role : Will check all roles for any issues or missing files.  Files will be generated using the `templates` folder.
- document_ansible : Will auto generate README.md files throughout the ansible project. (collections, roles, qtasks)

NOTE : if you create a new role, then run the check_role & document_roles scripts as well to complete the role with all necessary files and documentation.  
  
# Metadata

Metadata for documentation, such as description are found in :

- roles/<collection> : each collection has a `galaxy.yml` file with more info
- roles/<collection>/<role>/meta/main.yml : each role has a meta folder with a `main.yml` file containing :
    - role description : the description
    - supports multi : a boolean if role supports multi (looping lists of objects)
    - key : the key property of the role object (usually `name`)
- for `library` and `filter_plugins` a comment header is parsed