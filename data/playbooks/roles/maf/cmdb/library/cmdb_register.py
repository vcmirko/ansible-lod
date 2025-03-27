#!/usr/bin/python

# Copyright: (c) 2020, Mirko Van Colen <mirko@netapp.com>
# ==============================================================================
# DESCRIPTION
# This script is a blank template for custom logic, currently it does nothing and bypasses vars_external to the output
#
# VERSION HISTORY
# 2025-02-03 - Mirko Van Colen - Initial version
# ==============================================================================
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule


import datetime  # Import the datetime module



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
        cmdb                        = dict(type='dict', required=True), # cmdb dict
        user                        = dict(type='dict', required=True), # user
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
    cmdb           = module.params['cmdb']
    meta           = ve.get("meta", {})
    svm            = ve.get("svm", {})
    source         = ve.get("source", {})
    destination    = ve.get("destination", {})
    cluster_source = source.get("cluster", {})
    cluster_dest   = destination.get("cluster", {})
    user           = module.params['user']
    location       = meta.get("location", "")
    environment    = meta.get("environment", "")
    service        = meta.get("service", "")
    service_level  = meta.get("service_level", "")
    resource       = meta.get("resource", "")
    change_request = meta.get("change_request", "")
    mysql_host     = cmdb.get("host", "")
    mysql_user     = cmdb.get("user", "")
    mysql_password = cmdb.get("password", "")
    mysql_port     = cmdb.get("port", "")

    result         = {}

     # apply logic
    try:

        import pymysql

        # Open database connection
        db = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, port=mysql_port)

        # prepare a cursor object using cursor() method
        cursor = db.cursor()

        # insert data into log table
        sql = f"INSERT INTO `cmdb`.`log` (`created_at`, `location`, `environment`, `service`, `service_level`, `resource`, `change_request`, `customer`, `user`, `cluster`, `svm`) VALUES (CURRENT_TIMESTAMP, '{location}', '{environment}', '{service}', '{service_level}', '{resource}', '{change_request}', '{user}', '{cluster_source['name']}', '{svm}');"
        
        cursor.execute(sql)
        db.commit()
        db.close()

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
