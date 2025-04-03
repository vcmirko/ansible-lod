#!/usr/bin/python

# Copyright: (c) 2020, Mirko Van Colen <mirko@netapp.com>
# ==============================================================================
# DESCRIPTION
# This script is the custom logic used to create a volume advanced
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
    service        = meta.get("service", "").lower()
    service_level  = meta.get("service_level", "")
    change_request = meta.get("change_request", "")
    customer       = meta.get("customer", "").lower()
    name           = meta.get("name", "").lower()
    size           = meta.get("size", "")

    source         = ve.get("source", {})

     # apply logic
    try:

        # template
        log("Set templates")
        source["template"] = f"{service}_{service_level}"

        # create volume
        source["volume"] = {}
        source["volume"]["name"] = f"{location}_{environment}{service_level}_{service}_{customer}_{name}"
        source["volume"]["size"] = size
        source["volume"]["comment"] = f"Created by Ansible playbook {change_request}"
        source["volume"]["junction_path"] = f"/{source["volume"]["name"]}"

        # if smb, add cifs share
        if service == "smb":
            source["volume"]["cifs_share"] = {}
            source["volume"]["cifs_share"]["name"] = f"{name}$"
            source["volume"]["cifs_share"]["path"] = source["volume"]["junction_path"]

        # if nfs, add export policy
        if service == "nfs":
            source["export_policy"] = {}
            source["export_policy"]["name"] = f"xp_{name}"
        
            # auto add 0.0.0.0/0 to export policy for readonly
            rule = {}
            rule["client_match"] = "rhel1.demo.netapp.com"
            rule["ro_rule"] = "sys"
            rule["rw_rule"] = "sys"
            rule["super_user_security"] = "none"
            source["export_policy"]["rules"] = []
            source["export_policy"]["rules"].append(rule)

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
