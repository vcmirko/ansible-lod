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

        # open the file
        # remove first 3 lines
        # remove empty headers
        # keep only 20 first columns

        with open(file_path, mode='r', newline='') as file:
            csv_reader = csv.reader(file)
            data = []
            for row in csv_reader:
                data.append(row)

        # drop the first 3 lines
        data = data[3:]
        headers = data[0]
        data = data[1:]
        data = [dict(zip(headers[7:], row[7:22])) for row in data]

        # for now, only take the first 10 rows

        volumes = []
        volume = None
        for i in range(len(data)):
            # an aggr is given, we start a new volume dictionary
            
            if data[i]['lun']:

                if data[i]['aggr']:


                    # add the previous volume to the volumes list
                    if volume:
                        volumes.append(volume)

                    volume = {
                        'volume': data[i]['volume'],
                        'aggregate': {
                            'name': data[i]['aggr']
                        },
                        'space_guarantee': data[i]['Space Guarantee'],
                        'size': int(data[i]['vol-size']),
                        # volume.volume_autosize.maximum_size
                        'volume_autosize': {
                            'mode': data[i]['mode'],
                            'maximum_size': int(data[i]['max'])
                        },
                        'fractional_reserve': data[i]['reserve'],
                        'snapshot_autodelete': {
                            'enabled': data[i]['autodelete'] == 'true'
                        },
                        'snapshot_policy': {
                            'name': data[i]['snap policy']
                        },
                        'luns': []
                    }
                    
                lun = {
                    'name': data[i]['lun'],
                    'size': int(data[i]['lun-size']),
                    'os_type': data[i]['OS'],
                    'igroups': []
                }
                lun['igroups'].append(data[i]['igroup'])
                volume['luns'].append(lun)


        # add the last volume to the volumes list
        volumes.append(volume)


        ve['svm'] = {
            'name': data[0]['SVM']
        }
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
