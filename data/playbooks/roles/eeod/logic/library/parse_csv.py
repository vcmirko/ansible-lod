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


     # apply logic
    try:

        file_path = '/app/dist/persistent/playbooks/uploads/Epic Sizing_Cleveland Clinic_2020_v4(LUNs).csv'
        parsed_data = parse_csv(file_path)

        volumes = []

    #   aggregate_name                  : "{{ aggr_lookup.aggregate.name    | default(omit) }}"
    #   size                            : "{{ volume.size                   | default(omit) }}"
    #   size_unit                       : "{{ volume.size_unit              | default(omit) }}"
    #   space_guarantee                 : "{{ volume.space_guarantee        | default(omit) }}"
    #   percent_snapshot_space          : "{{ volume.percent_snapshot_space | default(omit) }}"
    #   wait_for_completion             : "{{ volume.wait_for_completion    | default(omit) }}"
    #   junction_path                   : "{{ volume.junction_path          | default(omit) }}"
    #   language                        : "{{ volume.language               | default(omit) }}"
    #   comment                         : "{{ volume.comment                | default(omit) }}"
    #   type                            : "{{ volume.type                   | default(omit) }}"
    # # atime_update                    : "{{ volume.atime_update           | default(omit) }}" # bad rest implementation
    #   compression                     : "{{ volume.compression            | default(omit) }}"
    #   encrypt                         : "{{ volume.encrypt                | default(omit) }}"
    #   group_id                        : "{{ volume.group_id               | default(omit) }}"
    #   inline_compression              : "{{ volume.inline_compression     | default(omit) }}"
    #   size_change_threshold           : "{{ volume.size_change_threshold  | default(omit) }}"
    #   unix_permissions                : "{{ volume.unix_permissions       | default(omit) }}"
    #   user_id                         : "{{ volume.user_id                | default(omit) }}"
    #   volume_security_style           : "{{ volume.security_style         | default(omit) }}"
    #   snaplock                        : "{{ volume.snaplock               | default(omit) }}"
    #   volume_space_logical_reporting  : "{{ volume.logical_space_reporting | default(omit) }}"
    #   volume_space_logical_enforcement: "{{ volume.logical_space_enforcement | default(omit) }}"
    #   efficiency_policy               : "{{ volume.efficiency_policy.name        | default(omit) }}"
    #   export_policy                   : "{{ volume.export_policy.name            | default(omit) }}"
    #   snapshot_policy                 : "{{ volume.snapshot_policy.name          | default(omit) }}"
    #   tiering_policy                  : "{{ volume.tiering_policy.name           | default(omit) }}"
    #   qos_policy_group                : "{{ volume.qos_policy_group.name         | default(omit) }}"
    # delegate_to: localhost
    # volume.snapshot_autodelete.enabled 
        volume = None
        for i in range(len(parsed_data)):
            # an aggr is given, we start a new volume dictionary
            
            if parsed_data[i]['aggr']:

                # add the previous volume to the volumes list
                if volume:
                    volumes.append(volume)

                volume = {
                    'volume': parsed_data[i]['volume'],
                    'aggregate': {
                        'name': parsed_data[i]['aggr']
                    },
                    'space_guarantee': parsed_data[i]['space-guarantee'],
                    'size': int(parsed_data[i]['vol-size']),
                    # volume.volume_autosize.maximum_size
                    'volume_autosize': {
                        'mode': parsed_data[i]['mode'],
                        'max': int(parsed_data[i]['max'])
                    },
                    'fractional_reserve': parsed_data[i]['reserve'],
                    'snapshot_autodelete': {
                        'enabled': parsed_data[i]['autodelete'] == 'true'
                    },
                    'snapshot_policy': {
                        'name': parsed_data[i]['snap-policy']
                    },
                    'luns': []
                }
                
            lun = {
                'name': parsed_data[i]['lun'],
                'size': int(parsed_data[i]['lun-size']),
                'os_type': parsed_data[i]['OS'],
                'igroups': []
            }
            lun.igroups.append(parsed_data[i]['igroup'])
            volume.luns.append(lun)
        
        # add the last volume to the volumes list
        volumes.append(volume)

     

        # convert parsed data to json
        parsed_data_json = json.dumps(parsed_data)
        log(parsed_data_json)

        ve['svm'] = parsed_data[0]['SVM']
        ve['volumes'] = volumes

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
