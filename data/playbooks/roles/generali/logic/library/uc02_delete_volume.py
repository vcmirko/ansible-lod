#!/usr/bin/python

# Copyright: (c) 2020, Mirko Van Colen <mirko@netapp.com>
# ==============================================================================
# DESCRIPTION
# The custom logic used to delete a volume
#
# It's setting the SVM & volume names based on the primary SVM & volume names
# and then removing the environments that are not needed based on the service level
#
# It's also making date-based new volume names for the rename action
# It's also removing the export policy name if it's the default one, to avoid deleting it
#
#
# VERSION HISTORY
# 2025-02-03 - Mirko Van Colen - Initial version
# ==============================================================================
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule

import datetime
import ansible.module_utils.generali as generali    # import generali module

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
    
    # grab metadata
    meta                               = ve.get('meta',{})
    volume_dr                          = meta.get('volume_dr') # '0' or '1'
    service_level                      = meta.get('service_level') # 'M1', 'M2', ...

    # grab the 3 environments
    primary                            = ve.get('primary',{}) # subkey of vars_external
    backup_local                       = ve.get('backup_local',{}) # subkey of vars_external
    backup_remote                      = ve.get('backup_remote',{}) # subkey of vars_external
    adpe                               = ve.get('adpe',{}) # subkey of vars_external

    # grab the 4 SVMs
    svm_primary                        = primary.get('svm',{})
    svm_backup_local                   = backup_local.get('svm',{})
    svm_backup_remote                  = backup_remote.get('svm',{})
    svm_adpe                           = adpe.get('svm',{})

    # grab the 4 volumes
    volume_primary                     = primary.get('volume',{})
    volume_backup_local                = backup_local.get('volume',{})
    volume_backup_remote               = backup_remote.get('volume',{})
    volume_adpe                        = adpe.get('volume',{})

    # grab the 4 export policies
    export_policy_primary              = primary.get('export_policy',{})
    # export_policy_backup_local         = backup_local.get('export_policy',{})
    # export_policy_backup_remote        = backup_remote.get('export_policy',{})
    # export_policy_adpe                 = adpe.get('export_policy',{})

    # grab the 3 snapmirrorsµ
    snapmirror_backup_local            = backup_local.get('snapmirror',{})
    snapmirror_backup_remote           = backup_remote.get('snapmirror',{})
    snapmirror_adpe                    = adpe.get('snapmirror',{})

    try:

        # timestamp yyyymmdd
        # make timestamp yymmdd
        timestamp = datetime.datetime.now().strftime("%y%m%d")

        # we don't touch the generic export policies
        if export_policy_primary["name"] == "XP_SMB_DEFAULT" or export_policy_primary["name"] == "XP_default":
            export_policy_primary.pop("name")


        # Set SVM names based on primary SVM name
        if svm_primary:
            log("Setting BL, BR and AP SVM names based on primary SVM name")
            svm_name = svm_primary['name']
            svm_backup_local['name'] = generali.get_resource_name(svm_name, "BL")
            svm_backup_remote['name'] = generali.get_resource_name(svm_name, "BR")
            svm_adpe['name'] = generali.get_resource_name(svm_name, "AP")
        else:
            raise Exception("Primary SVM is missing")

        # Set volume names based on primary SVM name
        if volume_primary:
            log("Setting BL, BR and AP volume names based on primary volume name")
            volume_name = volume_primary['name']
            volume_backup_local['name'] = generali.get_resource_name(volume_name, "BL")
            volume_backup_remote['name'] = generali.get_resource_name(volume_name, "BR")
            volume_adpe['name'] = generali.get_resource_name(volume_name, "AP")
        else:
            raise Exception("Primary volume is missing")

        # ---------------------
        # PRIMARY ENVIRONMENT
        # ---------------------

        # prep primary to create volume, export policy
        primary["export_policy"] = export_policy_primary

        # ---------------------
        # BACKUP LOCAL ENVIRONMENT
        # ---------------------

        volume_backup_local['old_name'] = volume_backup_local['name']
        volume_backup_local['name'] = f"{volume_backup_local['name']}_dism{timestamp}"
        # prep backup_local to create volume, export policy
        backup_local["volume"] = volume_backup_local

        # set destination for snapmirror
        snapmirror_backup_local["destination"]["svm"]["name"] = svm_backup_local["name"]
        snapmirror_backup_local["destination"]["volume"]["name"] = volume_backup_local["name"]

        backup_local["snapmirror"] = snapmirror_backup_local        

        # ---------------------
        # BACKUP REMOTE ENVIRONMENT
        # ---------------------

        volume_backup_remote['old_name'] = volume_backup_remote['name']
        volume_backup_remote['name'] = f"{volume_backup_remote['name']}_dism{timestamp}"
        # prep backup_remote to create volume, export policy
        backup_remote["volume"] = volume_backup_remote

        # set destination for snapmirror
        snapmirror_backup_remote["destination"]["svm"]["name"] = svm_backup_remote["name"]
        snapmirror_backup_remote["destination"]["volume"]["name"] = volume_backup_remote["name"]

        backup_remote["snapmirror"] = snapmirror_backup_remote

        # ---------------------
        # ADPE ENVIRONMENT
        # ---------------------

        # Todo: rename of adpe not possible
        # volume_adpe['old_name'] = volume_adpe['name']
        # volume_adpe['name'] = f"{volume_adpe['name']}_dism{timestamp}"
        # # prep adpe to create volume, export policy
        # adpe["volume"] = volume_adpe

        # set destination for snapmirror
        snapmirror_adpe["destination"]["svm"]["name"] = svm_adpe["name"]
        snapmirror_adpe["destination"]["volume"]["name"] = volume_adpe["name"]

        adpe["snapmirror"] = snapmirror_adpe

        # ---------------------
        # ASSEMBLE FINAL VARS
        # ---------------------

        ve["primary"] = primary
        ve["backup_local"] = backup_local
        ve["backup_remote"] = backup_remote
        ve["adpe"] = adpe

        # ---------------------
        # REMOVE ENVIRONMENTS BASED ON SERVICE LEVEL
        # ---------------------
        ve = generali.remove_unused_environments(ve, service_level, volume_dr)

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
