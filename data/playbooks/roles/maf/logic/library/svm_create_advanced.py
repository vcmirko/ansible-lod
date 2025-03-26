#!/usr/bin/python

# Copyright: (c) 2020, Mirko Van Colen <mirko@netapp.com>
# ==============================================================================
# DESCRIPTION
# This script is the custom logic used to create a SVM and volumes
#
# Adding a few lifs, setting volume junction paths and setting the template
#
# VERSION HISTORY
# 2025-02-03 - Mirko Van Colen - Initial version
# ==============================================================================
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
    meta           = ve.get("meta", {})

    location       = meta.get("location", "")
    environment    = meta.get("environment", "")
    service        = meta.get("service", "")
    service_level  = meta.get("service_level", "")
    resource       = meta.get("resource", "")
    change_request = meta.get("change_request", "")
    customer       = meta.get("customer", "")


    cluster        = ve.get("cluster", {})
    svm            = ve.get("svm", {})
    # volumes        = ve.get("volumes", [])

     # apply logic
    try:

        # validate input
        # validate_input([cluster, svm, volumes])

        # set template name
        svm["template"] = f"{service}_{service_level}" # set template name

        # complete svm lifs
        if svm.get("lifs", None):   
            svm["lifs"][0]["node"] = f"{cluster['name']}-01" # set node name

        # # loop over volumes and set junction path
        # for volume in volumes:
        #     volume["junction_path"] = f"/{volume['name']}"

        # reassign to vars_external
        ve["svm"] = svm 
        # ve["volumes"] = volumes

    except Exception as e:
        log(repr(e))
        err = str(e)

    result["vars"] = ve
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
