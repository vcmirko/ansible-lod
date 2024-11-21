#!/usr/bin/python

# Copyright: (c) 2020, Mirko Van Colen <mirko@netapp.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule

import csv
import json

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

def parse_csv(file_path):
    with open(file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        
        # Convert the remaining rows to a list of dictionaries
        data = [row for row in reader]
    
    return data

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

    file_path = '/app/dist/persistent/playbooks/uploads/Epic Sizing_Cleveland Clinic_2020_v4(LUNs).csv'
    parsed_data = parse_csv(file_path)

    # convert parsed data to json
    parsed_data_json = json.dumps(parsed_data)
    log(parsed_data_json)

     # apply logic
    try:

        pass

    except Exception as e:
        log(repr(e))
        err = str(e)

    result["vars"] = parsed_data
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
