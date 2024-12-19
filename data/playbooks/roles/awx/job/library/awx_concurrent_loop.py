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
            raise Exception("Missing required property awx_concurrent")
        
        # the awx_concurrent is a dict with 3 properties:
        # - template_name => the awx template we need to run concurrently
        # - list => the list of items to iterate over
        # - list_name => the name of the list item

        # the goal is to build a list with a copy of the vars_external dict, but with the list item added and the awx_concurrent dict removed

        # first we need to get the list of items
        list_items = ve.get(awx_concurrent['list'], None)
        if not list_items:
            raise Exception(f"Missing required property {awx_concurrent['list']}")
        
        # then we need to build the list
        list_name = awx_concurrent['list_name']
        for item in list_items:
            ve_copy = ve.copy()
            ve_copy[list_name] = item
            list.append(ve_copy)
            # remove the awx_concurrent dict
            ve_copy.pop('awx_concurrent', None)

    except Exception as e:
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
