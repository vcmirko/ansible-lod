# MAF - Mirko's Ansible Framework

## Playbooks

Each playbook looks fairly similar :

``` yaml
---
- name: "Create Volume nas"
  hosts: localhost
  become: false
  gather_facts: false
  vars_files:
    - "vars/defaults.yml"
    - "vars/templates.yml"
    - "vars/overrides.yml"

  roles:
    - { role: maf/facts, qtask: credentials }  
    - { role: maf/logic, qtask: my_logic }        # => this is the logic module, maf is the name of the customer
    - { role: ontap/volume, qtask: facts }
    - { role: ontap/volume, qtask: create }
    - { role: ontap/aiqum, qtask: facts }
    - { role: ontap/aiqum, qtask: rediscover }
```

Let's break it down :  

``` yaml
  hosts: localhost
  become: false
  gather_facts: false
```

Each playbook is targeted against localhost, no inventory is used.  We target ontap cluster from within the playbook.
Generally just 1 cluster, there are however exeptions in the case of snapmirror/snapvault that two or even 3 clusters are targets.
We don't gather_facts by default, as we target localhost and not much interesting information can be gathered.

``` yaml
  vars_files:
    - "vars/defaults.yml"
    - "vars/templates.yml"
    - "vars/overrides.yml"
```

Typically we load these 3 files that holds the defaults, templates and overrides.  
When testing, you can choose to load credentials and extravars from a file.  Wrap the extravars in a dict `vars_external`.
You can choose to load different files or have them together in 1 file.  
The main goal is to load 3 variables, which are mandatory:  **vars_defaults**, **vars_templates** and **vars_overrides**

``` yaml
  roles:
    - { role: maf/facts, qtask: credentials }  
    - { role: ontap/my_logic, qtask: facts }        
    - { role: ontap/volume, qtask: facts }
    - { role: ontap/volume, qtask: create }
    - { role: ontap/aiqum, qtask: facts }
    - { role: ontap/aiqum, qtask: rediscover }
```

Ansible has the concept "roles", that we use/abuse/reformat to create a somewhat readible workflow.  
In the example below we first :

- get the credentials
- process the logic
- create a volume  
- rediscover AIQUM.  

For each role we pass a subtask (variable `qtask`) that is part of that role.  
The task `facts` is a generic name for pre-processing variables aka `set_facts`.  
You will typically see this task for each role. (facts + create, facts + delete, facts + rename, fact + rediscover, ...).  
The goal of the facts task is to prepare the variables for the next task.  

## Variables and merging process

Ansible modules are fed information through variables.  In this framework, we try to structure these variables in objects/dicts.  
Throughout this documentation, we will use the example where we create a volume for cifs.  

``` yaml
volume:
    name                  : v_files_shared
    wait_for_completion   : true
    size                  : 10
    size_unit             : gb
    space_guarantee       : none
    percent_snapshot_space: 0
    comment               : "volume created for files, shared is enabled, change_request = CR123456"
    compression           : true
    junction_path         : /c_files_share
    security_style        : unix
    language              : c_utf8
svm:
    name                  : svm_cifs
cluster:
    name                  : na_ams_prod
    management_ip         : 10.0.0.1
```

Now some of this information will always be the same, some will be the same in certain cases, some will be calculated values, some will need to be looked up, ...
The concept of this framework is to merge 4 layers of information to build the final object.  

To make the framework dynamic we use a couple of variables in this framework that each contain a layer of information :  

- vars_defaults
- vars_templates
- vars_local (after vars_external have been processed by the logic-module)
- vars_overrides

### vars_defaults

Holds default information per object type (svm, volume, ...)

**Example** :

``` yaml
vars_defaults:
    volume:
        wait_for_completion    : true
        size_unit              : gb
        space_guarantee        : none
        language               : c_utf8
        security_style         : unix
        compression            : true
        percent_snapshot_space : 0
```

### vars_templates

Holds specific information per object type (svm, volume, ...) grouped together in a **template**, typically for a specific use case.  
Templates might have overlapping pieces of information, hence the use of **anchors** and **aliases** might be a good idea.

**Example** :  

``` yaml
vars_templates:
    nas_nfs:                                # this is the template name 
        volume:                             # object volume for this specific template
            security_style         : unix   
            percent_snapshot_space : &percent_snapshot_space 10 # working with anchors is perfect for these templates
        svm:
            allowed_protocols: nfs

    nas_cifs:                               # another template
        volume:
            security_style         : ntfs
            percent_snapshot_space : *percent_snapshot_space 
        svm:
            allowed_protocols: cifs
```  

### vars_external

Holds information from external/operator, aka the extra_vars, they must however be wrapped in 1 parent dict `vars_external`.  
  
**Example 1** : Logic is handled external, naming conventions external, resource selection is external.  
Note the template name `nas_cifs` is passed.

``` yaml
vars_external:
    template: nas_cifs
    volume:
        name          : v_files_shared_001
        size          : 10
        junction_path : /v_files_shared_001
        comment       : "volume created for files, shared is enabled, change_request = CR123456"
    svm:
        name: svm_cifs
    cluster:
        name          : na_ams_prod
        management_ip : 10.0.0.1
```  

**Example 2** : Logic is handled internal, naming conventions internal, resource selection is internal.  The input in this case is somewhat customer specific.  A good practice is to put it under something meaningfull, in this case `meta` (short for metadata)

``` yaml
vars_external:
    meta:
        environment : prod
        location    : ams
        service     : files
        shared      : true
        change_req  : CR123456
    volume:
        size        : 9
```  

## vars_local

Holds the reworked information where vars_external has been processed by the logic-module.  
Typically in the logic-modules the incoming data is being :

- **validated** : perhaps you want to check required information or check formatting, ...
- **analysed** : apply some if-then-else logic, custom function, ...
- **completed** : maybe some resource-selection is required, rest-calls, database lookups, ... to complete the data
- **reworked** : some input data can be modified, removed, added, naming conventions can be applied, ...

**Note** : extra_vars in ansible are immutable.  Since vars_external are extra_vars, we must host the reworked data in a new dict `vars_local`.

**Example1**: The logic-task to, for example, delete a lun.  When a lun is deleted, the customer wants it renamed to `del_{{ lunname }}`.  Since this is customer specific, we will put this in a custom logic-module.

``` yaml
# apply logic for the lun_delete operation
- lun_delete:  # => this is a custom module to handle the logic for lun_delete operation
    vars_external : "{{ vars_external }}" # => external variables go in (vars_external)
  delegate_to: localhost
  register: logic_result 

# debug the result of the logic if needed
- debug: var=logic_result 
  verbosity: 2

# store the processed data in vars_local
- set_fact:
    vars_local : "{{ logic_result.vars }}" 
```

**Example2**: The logic-task to create a share.  The share will land on a specific svm, based on the service.  The volume name will be created based on the service, shared, and an auto-increment number.  The junction path will be created based on the volume name.  The comment will have the change_request number added.  We pass, next to the vars_external, the aiqum credentials and the mysql credentials.  The logic will look up the svm, the cluster, ...  

``` yaml
## Naming facts
- facts_share:
    vars_external : "{{ vars_external }}"
    aiqum_host    : "{{ aiqum_host }}"
    aiqum_username: "{{ aiqum_username }}"
    aiqum_password: "{{ aiqum_password }}"
    mysql_host    : "{{ mysql_host }}"
    mysql_username: "{{ mysql_username }}"
    mysql_password: "{{ mysql_password }}"
    mysql_port    : "{{ mysql_port }}"
  delegate_to: localhost
  register: logic_result

# - debug: var=logic_result

- set_fact:
    vars_local : "{{ logic_result.vars }}"
```

If the logic is done outside, then `vars_local` can be just a copy of `vars_external`.  Or use the `bypass` module to skip the logic.

**Example** : Below is the vars_local after the logic has been applied.  

``` yaml
# this is the vars_local after the logic has been applied
vars_local:
    template: nas_cifs     # the templatename is added
    volume:
        name          : v_files_shared_001     # the volume name is created "v_%service%_%shared%_%auto_incr_nr%"
        size          : 10                     # the size is rounded to a multitide of 10
        junction_path : /v_files_shared_001    # the junction path is create "/%volumename%"
        comment       : "volume created for files, shared is enabled, change_request = CR123456"  # CR number added in the comment
    svm:
        name: svm_cifs # svm resource has be looked up, an svm serving cifs is found
    cluster:
        name          : na_ams_prod   # the cluster resource is found base on location and environment
        management_ip : 10.0.0.1
```  

### vars_overrides

As an extra layer we can apply overrides, certain values that need to be set, no matter what.  
This could be used in the case of a demo, or test environment where you want temporarily override certain values.
In a test environment for example, you can choose to set the size_unit to mb instead of gb, or use a different active directoy and dns server.  
It's also a way to enforce certain values, like setting the security style to ntfs for all volumes, no matter what the template says or what the logic has calculated or the operator has passed.  

``` yaml
vars_overrides:
    volume:
        size_unit              : mb
        security_style         : ntfs
```

## merging process

In every role, the variables are merged in the following order :  

- vars_defaults
- vars_templates
- vars_local (after being processed by the logic-module)
- local object (in case we are in a loop, the loop item)
- vars_overrides

This merging process is done in the `facts` task of each role.

**Example 1**: A normal merging process

``` yaml
- name: Merge Extravars
  ansible.builtin.set_fact:
    export_policy: "{{ 'export_policy' | merge_vars(d=vars_defaults,t=vars_templates,v=vars_local,o=vars_overrides,c=qtask_child) }}"
    svm          : "{{ 'svm'           | merge_vars(d=vars_defaults,t=vars_templates,v=vars_local,o=vars_overrides,c=qtask_child) }}"
    cluster      : "{{ 'cluster'       | merge_vars(d=vars_defaults,t=vars_templates,v=vars_local,o=vars_overrides,c=qtask_child) }}"
```

**Example 2**: A loop item is added to the local object

``` yaml
- name: Merge Extravars
  ansible.builtin.set_fact:
    # note in volume, l = volume_item => the volume role implements multiple => volume_item is the loop item, which is merged too.
    # because it is undefined when running single => you must default it.
    volume : "{{ 'volume'      | merge_vars(d=vars_defaults,t=vars_templates,v=vars_local,l=volume_item,o=vars_overrides,c=qtask_child) }}"
    svm    : "{{ 'svm'         | merge_vars(d=vars_defaults,t=vars_templates,v=vars_local,o=vars_overrides,c=qtask_child) }}"
    cluster: "{{ 'cluster'     | merge_vars(d=vars_defaults,t=vars_templates,v=vars_local,o=vars_overrides,c=qtask_child) }}"
```

**Example 3**: There is a list to merged, you will typically see this in the case of a loop, in the `facts_multi` task

``` yaml
- name: Merge Extravars
  ansible.builtin.set_fact:
    volumes : "{{ 'volumes' | merge_lists(v=vars_local,required_keys=['name'],c=qtask_child) }}"
```

## Multiple plays in a playbook / qtask_child

In the case of multiple plays in a playbook, we need to pass the child task to the merge_vars function.  
Imagine, you want to target 2 clusters (create volume and it's snapvault destination), you will have 2 plays in the playbook.  
In our vars_external, we will have objects for 2 enviroments.  So we need to make a sub-object.

``` yaml
vars_external:
    source: # => a sub object to hold the source enviroment
        template: nas_cifs
        cluster:
            name          : na_ams_prod
            management_ip :
        volume:
            name          : v_files_shared_001
        svm:
            name: svm_cifs
    destination: # => a sub object to hold the destination enviroment
        template: nas_dr
        cluster:
            name          : na_ams_dr
            management_ip :
        volume:
            name          : v_files_shared_001_vault
        svm:
            name: svm_cifs_dr
```

The playbook will look like this :

``` yaml
---
- name: "Create Volume nas"
  hosts: localhost
  become: false
  gather_facts: false
  vars_files:
    - "vars/defaults.yml"
    - "vars/templates.yml"
    - "vars/overrides.yml"

  roles:
    - { role: maf/facts, qtask: credentials }  
    - { role: maf/logic, qtask: facts }
    - { role: ontap/volume, qtask: facts, qchild: source }
    - { role: ontap/volume, qtask: create, qchild: source }

- name: "Create the Dr volume"
  hosts: localhost
  become: false
  gather_facts: false
  vars_files:
    - "vars/defaults.yml"
    - "vars/templates.yml"
    - "vars/overrides.yml"

  roles:
    - { role: maf/facts, qtask: credentials }  
    - { role: maf/logic, qtask: facts }
    - { role: ontap/volume, qtask: facts, qchild: destination }
    - { role: ontap/volume, qtask: create, qchild: destination }

- name: "Rediscover aiqum on both sides"
  hosts: localhost
  become: false
  gather_facts: false
  vars_files:
    - "vars/defaults.yml"
    - "vars/templates.yml"
    - "vars/overrides.yml"

  roles:
    - { role: maf/facts, qtask: credentials }  
    - { role: maf/logic, qtask: facts }
    - { role: ontap/aiqum, qtask: facts, qchild: source }
    - { role: ontap/aiqum, qtask: rediscover, qchild: source }
    - { role: ontap/aiqum, qtask: facts, qchild: destination }
    - { role: ontap/aiqum, qtask: rediscover, qchild: destination }
```

## Roles

The roles are structured in a way that they can be used in playbook with some reusability, flexibility and readability.  
Using the `qtask` variable, we can choose which task to execute in the role.  

Also notice the subdirectory of the role.

- maf/logic : maf is a folder (representing the customer maf) that will hold the roles for that customer.  In this case the logic role.
- ontap/volume : ontap is a folder that holds the netapp roles.  In this case the volume role.

You can create your own roles, just make sure to follow the structure. (vmware, cyberark, ...)

### Tasks

Each role has at least 3 tasks :

- **main.yml** : this is the entry point for the role, it will call the facts, create, delete, rename, ... task.  
- **facts.yml** : this is the task that will prepare the variables for the next task.  It will merge the variables.
- **create.yml** : this is the task that will execute the create operation.  It will call the module to create.  It does not need to be "create", give it a logical name that fits the operation.

**The main.yml** : will also access qtaks_description, qtask_suffix, qtask_child, ... you can extend the variables as needed.

``` yaml
---
include_tasks: "{{ qtask }}.yml"
  vars:
    qtask_description: "{{ qdesc | default('') }}" # you can add a custom description to the role-task
    qtask_suffix: "{{ qsuffix | default('') }}"    # you can add a custom suffix to the role-task in case your object has a suffix (volume1, volume2, ..., volume_source, volume_destination, ...) => you can then pass respectively (1, 2, _source, _destination, ...)  The merge_vars function accepts this suffix as variable 's' and will append it to the name.
    qtask_child: "{{ qchild | default('') }}"      # if will be used in the merge_vars function to pass a child-object name.
```

**The facts.yml** :

``` yaml
---
## Naming facts
- name: Merge Extravars
  ansible.builtin.set_fact:
    unix_user: "{{ 'unix_user'  | merge_vars(d=vars_defaults,t=vars_templates,v=vars_local,o=vars_overrides,c=qtask_child) }}"
    svm      : "{{ 'svm'        | merge_vars(d=vars_defaults,t=vars_templates,v=vars_local,o=vars_overrides,c=qtask_child) }}"
    cluster  : "{{ 'cluster'    | merge_vars(d=vars_defaults,t=vars_templates,v=vars_local,o=vars_overrides,c=qtask_child) }}"

# - name: debug cifs share after merge
#   debug:
#     var: unix_user


- name: Set naming facts
  ansible.builtin.set_fact:
    # ansible_python_interpreter:   /usr/bin/python3
    netapp_hostname:                "{{ cluster.management_ip }}"
    netapp_username:                "{{ ontap_username }}"
    netapp_password:                "{{ ontap_password }}"
    svm_name:                       "{{ svm.name }}"
    unix_user_name:                 "{{ unix_user.name      | default(omit) }}"
    unix_user_full_name:            "{{ unix_user.full_name | default(omit) }}"
    unix_user_group_id:             "{{ unix_user.group_id  | default(omit)}}"
    unix_user_id:                   "{{ unix_user.id        | default(omit)}}"
  delegate_to: localhost
```

### Process multiple objects

Sometimes you need to process multiple objects, like creating multiple volumes, deleting multiple luns, ...  
We still want to use the merging process on item level, so we need wrap this in a loop.  In this case we use the `facts_multi` task and `create_multi` task (or delete_multi, ...).  

In the example of `volume`, we will have a list of `volumes` in vars_local.  We will loop over this list and process each volume.  
  
The `facts_multi.yml` will look like this :

``` yaml
## Naming facts
- name: Merge Extravars
  ansible.builtin.set_fact:
    volumes : "{{ 'volumes' | merge_lists(v=vars_local,required_keys=['name'],c=qtask_child) }}"
```

Note that we also process the `qtask_child`.  Optionally you can pass a list of required_keys, this will check if the key is present in the object.

The `create_multi.yml` will look like this :

``` yaml
- name: Create multiple volumes
  include_tasks: "create_one.yml" 
  loop_control:
    loop_var: volume_item
    label: "Creating volume {{ volume_item.name }}"
  loop: "{{ volumes }}"
```

The loop will call the `create_one.yml` task, which will look like this :

``` yaml
---
- include_tasks: "facts.yml"
- include_tasks: "create.yml"
```

This way we can process multiple objects in a role and still use the merging process.
