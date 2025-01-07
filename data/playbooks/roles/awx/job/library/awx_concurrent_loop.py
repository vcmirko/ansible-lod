#!/usr/bin/python

# Copyright: (c) 2020, Mirko Van Colen <mirko@netapp.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule

summary=[]
result = {}

def validate_input(inputs):
    for i in inputs:
        for key in i:
            if not i[key]:
                raise Exception(f"Missing required parameter {key}")

# logging 
def log(t):
    global summary
    summary.append(t)

# main code
def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        # debug                     = dict(type='bool', required=False, default=False),
        vars_external               = dict(type='dict', required=True), # vars external dict
  
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # store input to vars, some are global
    global summary
    
    err = None
    # debug          = module.params['debug']
    ve             = module.params['vars_external']
    awx_concurrent = ve.get('awx_concurrent', None)
    list = []

     # apply logic
    try:

        if not awx_concurrent:
            raise Exception("Missing required property 'awx_concurrent'")

        # first we need to get the list of items
        list_items = awx_concurrent.get('list', None)

        if not list_items:
            raise Exception(f"Missing required property 'list'")

        list_name = awx_concurrent.get('list_name', None)

        if not list_name:
            raise Exception(f"Missing required property 'list_name'")
        
        list_label = awx_concurrent.get('list_label', None)

        if not list_label:
            raise Exception(f"Missing required property 'list_label'")

        for item in list_items:

            ve_copy = ve.copy()
            ve_copy[list_name] = item
            ve_copy['awx'] = {}
            ve_copy['awx']['name'] = awx_concurrent['template_name']
            ve_copy['awx']['concurrent_label'] = item[awx_concurrent['list_label']]
            # can be extended with more awx parts 
            list.append(ve_copy)
            # remove the awx_concurrent dict
            ve_copy.pop('awx_concurrent', None)

    except Exception as e:
        print("Error happened")
        log(repr(e))
        err = str(e)

    result["vars"] = list
    result["summary"] = summary

    # return
    if err:
        module.fail_json(err,**result)
    else:
        module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
