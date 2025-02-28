# MAF - Modular Ansible Framework

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

Each playbook is targeted against localhost, no inventory is used.  We target ontap clusters from within the playbook.  Generally just 1 cluster, there are however exeptions in the case of snapmirror/snapvault that two or even 3 clusters are targets.
We don't `gather_facts` by default, as we target localhost and not much interesting information can be gathered.
  
**Note** : An inventory can be useful is certain cases, like typical multi cluster tasks.  Since we set `delegate` to `localhost`, an inventory will still work.

``` yaml
  vars_files:
    # - "vars/test_credentials.yml" => inject / or lookup in production
    - "vars/defaults.yml"
    - "vars/templates.yml"
    # - "vars/test_extravars.yml" => inject in production
    - "vars/overrides.yml"
```

Typically we load 3 files that hold the **defaults**, **templates** and **overrides**.  
  
When testing, you can choose to load test-credentials and test-extravars from a file.  Wrap the extravars in a dict `vars_external`.
You can choose to load different files, custom files or have them together in 1 file.  
  
The main goal is to load 4 variables, which are mandatory:  **vars_defaults**, **vars_templates**, **vars_external**, and **vars_overrides**  

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
  
In the example above we :

- get the credentials
- process the logic
- create a volume  
- rediscover AIQUM.  

For each role we pass a subtask/subrole (using variable `qtask`) that is part of that role.  
  
The `qtask` variable is a MAF-specific variable we use to tell the role which subtask to perform.  This way we can segregate several actions within a role.

The task `facts`, that keeps recurring, is a generic name for pre-processing variables aka `set_facts`.  
  
You will typically see this task before each role. (facts + create, facts + delete, facts + rename, fact + rediscover, ...).  
The goal of the facts task is to prepare the variables for the next task.  In the case of NetApp ONTAP, we will typically prepare the hostname, usually (but not always) a `cluster.management_ip`, with a fallback to `ansible_host` in case there is an inventory.

## Variables and merging process

Ansible modules are receiving information through variables.  And it's true, ansible has a hierarchy of precedence with vars folders and defaults etc... 

Howewever, this only works for single variables.  In more complex environments, we want to use objects/dicts.  And the precedence doesn't work with dicts.  

In this framework, we try to structure these variables in objects/dicts and use a **custom written filter** that can merge dicts on a property level.  

Throughout this documentation, we will use the example where we create a volume for cifs.  

Let's assume the following payload (extravars), is passed to the playbook.

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

When we analyse this payload, some of this information will :

- always be the same, 
- will be the same in certain cases, 
- will be calculated values, 
- will need to be looked up, 
- ...

The concept of this framework is to merge 4 layers of information to build the final object.  

To make the framework dynamic we use a couple of variables in this framework that each contain a layer of information :  

- vars_defaults
- vars_templates
- vars_local (after vars_external have been processed by the logic-module, vars_external is transformed to vars_local)
- vars_overrides

### vars_defaults

Holds default information per object type (svm, volume, ...)

**Example** :  

  
Most of customers will have a least a few defaults.

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

Templates might have overlapping pieces of information, hence the use of **anchors** and **aliases** might be a good idea. (https://support.atlassian.com/bitbucket-cloud/docs/yaml-anchors/)

**Example** :  

Most customers will have use-cases where templates will come in handy.

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
            percent_snapshot_space : *percent_snapshot_space # here we use an alias to inject the data from the previous anchor
        svm:
            allowed_protocols: cifs
```  

### vars_external

Holds information from external (operator, cli, ...), aka the extra_vars, they must however be wrapped in 1 parent dict `vars_external`.  
  
**Example 1** : Logic is handled external, naming conventions external, resource selection is external.  

**Note** : the template name `nas_cifs` is passed.  
**Note** : the template can also be placed on object-level (eg. volume)

``` yaml
vars_external:
    template: nas_cifs # apply template
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

**Example 2** : Logic is handled internally, naming conventions internal, resource selection is internal.  The input in this case is somewhat customer specific.  

A good practice is to put it under something meaningfull, in this case `meta` (short for metadata).  

The logic can be applied with jinja2-filter, jinja2-templates, or, a personal favorite, a custom module, where we have the full python libraries at our disposal.  This custom module will take the vars_external and manipulate it with resource selections, environment decisions and naming conventions.

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

**Example 3** : The external extra_vars are not structured and will need to be preprocessed even more.

``` yaml
  environment : prod
  location    : ams
  service     : files
  shared      : true
  change_req  : CR123456
  volume_size : 9
```  

In this case, we will most likly do a 2-step preprocessing. 

- Pass the information through a jinja2-template, adding a bit of structure
- Pass the information through an ansible-module to complete more complex logic.


## vars_local

Holds the reworked information where vars_external has been processed by the logic-module.  
Typically in the logic-modules the incoming data is being :

- **validated** : perhaps you want to check required information or check formatting, ...
- **analysed**  : apply some if-then-else logic, custom function, ...
- **completed** : maybe some resource-selection is required, rest-calls, database lookups, ... to complete the data
- **reworked**  : some input data can be modified, removed, added, naming conventions can be applied, ...

**Note** : extra_vars in ansible are immutable (read-only).  Since we want to add/modify/remove the input data, we createa new dict `vars_local`.

**Example**: This is a full example, starting with unstructured extra_vars.
  
``` yaml
---
- name: "Role - customerX/logic/logicX"
  block:

  ## Assemble vars_external from unstructured input
  - name: "Convert input to vars_external"
    set_fact:
      vars_external: "{{ lookup('template', '../templates/logicX.yml.j2', convert_data=False) | from_yaml }}"

  ## Apply further logic to the now-structured-data
  - name: "Logic - logicX" 
    logicX:
      vars_external : "{{ vars_external }}"
    delegate_to: localhost
    register: logic_result

  - name: Register logic result
    set_fact:
      vars_local : "{{ logic_result.vars }}"

  - name: Logging
    set_fact:
      qlogname: "{{ vars_external | to_nice_yaml(2) | indent(2,true) | do_log('Running logic logicX','vars_external',qlogname) }}"

  - name: Logging
    set_fact:
      qlogname: "{{ vars_local | to_nice_yaml(2) | indent(2,true) | do_log('After logic logicX','vars_local',qlogname) }}"
```

Note that we can also log the before (vars_external) and after (vars_logic) into some logfile.  
If the logic is done outside, then `vars_local` can be just a copy of `vars_external`.  Or use the `bypass` module in collection `maf` to skip the logic.

**Example data** : Unstructured data -> structured data -> logic process -> output

Unstructed input :

``` yaml
# extra_vars received
SVC     : FILES
SVC_TYPE: SHARED
PROT    : CIFS
SZ      : 9
CR      : CR123456
LOC     : AMS
ENV     : PROD
```

Jinja2 template : will add some structure and a apply some basic logic.    
Hint : try to keep the logic within the jinja step to a minimum, for readibility  
  
``` yaml
# file ./templates/logicX.yml.j2
vars_external:
  meta: 
    service       : "{{ SVC      | default('files')  | lower }}" 
    service_type  : "{{ SVC_TYPE | default('shared') | lower }}"
    protocol      : "{{ PROT     | default('nfs')    | lower }}"
    change_request: "{{ CR       | default('')       | upper }}"
    location      : "{{ LOC      | default('bru')    | lower }}"
    environment   : "{{ ENV      | default('dev')    | lower }}"
  volume:
    size: "{{ SZ | int }}"
```

Below a sample code snippet, applying further logic

``` python
# file ./library/logicX.py
# ... this is just a snippet of a custom logic module 

# grab input
ve                                 = module.params['vars_external']

# grab metadata
meta                               = ve.get('meta')
service                            = meta.get('service')
service_type                       = meta.get('service_type')
protocol                            = meta.get('protocol')
change_request                      = meta.get('change_request')
location                            = meta.get('location')
environment                         = meta.get('environment')

# prep resources
cluster                            = ve.get('cluster',{})
svm                                = ve.get('svm',{})
volume                             = ve.get('volume',{})

# apply logic
resource = find_proper_cluster(location,environment) # just an example to find a resource based on location & environment
cluster["name"]          = resource["cluster_name"]
cluster["management_ip"] = resource["cluster_ip"]

svm["name"] = f"svm_{protocol}"

volume["name"]          = find_next_incremental_name(f"v_{service}_{service_type}_###",'001') # function that finds next incremental name, default = 001
volume["comment"]       = f"volume created for {service}, {service_type} is enabled, change_request = {change_request}"
volume["junction_path"] = f"/{volume["name"]}" 
volume["size"]          = (volume["size"] + 9) // 10 * 10 # round to next 10

# assemble
ve["template"]= f"nas_{protocol}"
ve["meta"]    = meta
ve["cluster"] = cluster
ve["svm"]     = svm
ve["volume"]  = volume

```

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
    dns:
        domain: demo.local
        servers: 192.168.1.1
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

**Example 3**: There is a list to be merged, you will typically see this in the case of a loop, in the `facts_multi` task

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
