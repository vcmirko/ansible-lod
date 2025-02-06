#!/usr/bin/python

# Copyright: (c) 2020, Mirko Van Colen <mirko@netapp.com>
# ==============================================================================
# DESCRIPTION
# The custom logic used to resize a quota
#
# It's only purpose is setting the quota target based on the volume & qtree name
#
# VERSION HISTORY
# 2025-02-03 - Mirko Van Colen - Initial version
# ==============================================================================
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
import re

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

    # grab input
    ve                                 = module.params['vars_external']

   
    # grab the 3 environments
    primary                            = ve.get('primary',{}) # subkey of vars_external
    quota                              = primary.get('quota',{}) # subkey of primary
    volume                             = primary.get('volume',{}) # subkey of primary
    qtree                              = primary.get('qtree',{}) # subkey of primary

    try:

        # set quota target
        volume_name = volume.get('name','')
        qtree_name = qtree.get('name','')
        quota["quota_target"] = f"/vol0/{volume_name}/{qtree_name}"
        primary["quota"] = quota

        # ---------------------
        # ASSEMBLE FINAL VARS
        # ---------------------

        ve["primary"] = primary

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
