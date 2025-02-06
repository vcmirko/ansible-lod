#!/usr/bin/python

# Copyright: (c) 2020, Mirko Van Colen <mirko@netapp.com>
# ==============================================================================
# DESCRIPTION
# The custom logic used to create a volume
#
# It's setting the SVM & volume names based on the primary SVM & volume names
# and then removing the environments that are not needed based on the service level & volume_dr
#
# Setting the export policy name based on the volume style
# Creating a CIFS share if the volume style is SMB or MIX
# Settings proper ACL's on the CIFS share
# Add template to the CIFS share to apply properties from the templates_generali.yaml file
# -> to add the CIFS share properties like access_based_enumeration, oplocks, ...
# -> Used to be passed by vrealize, but now it's hardcoded in the templates_generali.yaml file
# -> Old values were zapi based and not working for rest api
# When is_ivz is True, no export policy rules are set, this is for Germany only and has its own rules
# Adding junction path to the volume
# Adding adaptive QoS policy to the volume
# Disabling autosize if needed
# Setting snapshot policy's
# Setting snapmirror policy's and schedules 
# Adpe has a different snapmirror policy and schedule (fixed VP_30 and ADPE schedule)
#
# VERSION HISTORY
# 2025-02-03 - Mirko Van Colen - Initial version
# ==============================================================================
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
import ansible.module_utils.generali as generali
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
    
    # grab metadata
    meta                               = ve.get('meta',{})
    volume_style                       = meta.get('volume_style') # 'SMB', 'NFS', 'MIX'
    volume_junction                    = meta.get('volume_junction')
    volume_performace_class            = meta.get('volume_performace_class') # 'A', 'B', ..
    volume_autosize                    = meta.get('volume_autosize') # true/false
    volume_dr                          = meta.get('volume_dr') # '0' or '1'
    country                            = meta.get('country')
    data_type                          = meta.get('data_type') # 'APP', ...
    snapmirror_policy                  = meta.get('snapmirror_policy') # 'VP_30D', ...
    service_level                      = meta.get('service_level') # 'M1', 'M2', ...
    is_ivz                             = meta.get('is_ivz') # True or False

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
    export_policy_primary              = primary.get('export_policy',{}) # export policy => primary has no rules
    export_policy_backup_local         = backup_local.get('export_policy',{}) # export policy => has rules if NFS/MIX and not is_ivz
    export_policy_backup_remote        = backup_remote.get('export_policy',{}) # export policy => has rules if NFS/MIX and not is_ivz
    export_policy_adpe                 = adpe.get('export_policy',{}) # export policy => has rules if NFS/MIX and not is_ivz

    # grab the 3 snapmirrors
    snapmirror_backup_local            = backup_local.get('snapmirror',{})
    snapmirror_backup_remote           = backup_remote.get('snapmirror',{})
    snapmirror_adpe                    = adpe.get('snapmirror',{})

    try:

        # export policy
        export_policy_name = ""
        if volume_style == 'NFS' or volume_style == 'MIX':
            export_policy_name = f"XP_{volume_junction}"
        elif volume_style == 'SMB':
            export_policy_name = f"XP_SMB_DEFAULT"

        # make copy of export_policy for backup_local or backup_remote.
        # only keep rules if NFS/MIX and not is_ivz
        
        export_policy_primary["name"] = export_policy_name
        export_policy_backup_local["name"] = export_policy_name
        export_policy_backup_remote["name"] = export_policy_name
        export_policy_adpe["name"] = export_policy_name

        export_policy_primary.pop('rules',None)           # primary has no export rules
        
        # ivz = germany, no export policy rules (has its own rules)
        if (volume_style == 'NFS' or volume_style == 'MIX') and not is_ivz:
            pass
        else:
            log("Removing export policy rules for backup, not NFS/MIX or is_ivz")
            export_policy_backup_local.pop('rules',None) # remove rules            
            export_policy_backup_remote.pop('rules',None) # remove rules

        # junction path
        junction_path = f"/{volume_junction}"

        # cif share
        cifs_share = {}
        # cifs share
        if volume_style == 'SMB' or volume_style == 'MIX':

            log("Volume style is SMB or MIX, creating CIFS share")

            cifs_share["name"] = f"{country}_{volume_style}_{data_type}_{volume_junction}$"
            cifs_share["path"] = f"/{volume_junction}"

            # acls
            cifs_share["acls"] = []

            # remove everyone full control
            log("Removing everyone full control ACL")
            everyone_acl = generali.get_admin_acl('')
            cifs_share["acls"].append(everyone_acl)

            # add global admin
            log("Adding global admin ACL")
            default_acl = generali.get_admin_acl('default')
            cifs_share["acls"].append(default_acl)

            # add country admin
            country_acl = generali.get_admin_acl(country)
            log("Country ACL is " + str(country_acl))

            if country_acl:
                cifs_share["acls"].append(country_acl)    

            # apply to all environments
            primary["cifs_share"] = cifs_share    
            primary["cifs_share"]["template"] = "primary" # apply cifs share properties using template
            backup_local["cifs_share"] = cifs_share.copy()
            backup_local["cifs_share"]["template"] = "backup_local" # apply cifs share properties using template
            backup_remote["cifs_share"] = cifs_share.copy()
            backup_remote["cifs_share"]["template"] = "backup_remote" # apply cifs share properties using template


        # Set SVM names based on primary SVM name
        if svm_primary:
            log("Setting BL, BR and AP SVM names based on primary SVM name")
            svm_name = svm_primary['name']
            svm_backup_local['name'] = generali.get_resource_name(svm_name, "BL")
            svm_backup_remote['name'] = generali.get_resource_name(svm_name, "BR")
            svm_adpe['name'] = generali.get_resource_name(svm_name, "AP")
        else:
            raise Exception("SVM not found for primary")

        # Set volume names based on primary SVM name
        if volume_primary:
            log("Setting BL, BR and AP volume names based on primary volume name")
            volume_name = volume_primary['name']
            volume_backup_local['name'] = generali.get_resource_name(volume_name, "BL")
            volume_backup_remote['name'] = generali.get_resource_name(volume_name, "BR")
            volume_adpe['name'] = generali.get_resource_name(volume_name, "AP")
        else:
            raise Exception("Volume not found for primary")

        # ---------------------
        # PRIMARY ENVIRONMENT
        # ---------------------


        volume_primary['qos_adaptive_policy_group'] = {}
        volume_primary['qos_adaptive_policy_group']["name"] = f"{svm_primary['name']}_QOP_CLASS_{volume_performace_class}"
        volume_primary['export_policy'] = export_policy_primary 
        volume_primary['junction_path'] = junction_path

        log("Primary autosize is " + str(volume_autosize))

        # disable autosize if needed
        if volume_autosize == False:

            log("Disabling autosize for primary")
            # remove autosize from dict
            volume_primary.pop('autosize')

        # prep primary to create volume, export policy
        primary["volume"] = volume_primary
        primary["export_policy"] = export_policy_primary


        # ---------------------
        # BACKUP LOCAL ENVIRONMENT
        # ---------------------
           
        volume_backup_local['qos_adaptive_policy_group'] = {}
        volume_backup_local['qos_adaptive_policy_group']["name"] = f"{svm_backup_local['name']}_QOP_CLASS_{volume_performace_class}"
        volume_backup_local['export_policy'] = export_policy_backup_local
        volume_backup_local['junction_path'] = junction_path

        # set snapshot policy to none
        log("Setting snapshot policy to none for backup_local")
        volume_backup_remote['snapshot_policy'] = {}
        volume_backup_remote['snapshot_policy']["name"] = "none"

        # prep backup_local to create volume, export policy
        backup_local["volume"] = volume_backup_local
        backup_local["export_policy"] = export_policy_backup_local

        # set snapmirror policy and schedule
        snapmirror_backup_local["policy"] = snapmirror_policy
        snapmirror_backup_local["schedule"] = "daily_vault"

        # set destination for snapmirror
        snapmirror_backup_local["destination"]["svm"]["name"] = svm_backup_local["name"]
        snapmirror_backup_local["destination"]["volume"]["name"] = volume_backup_local["name"]

        backup_local["snapmirror"] = snapmirror_backup_local

        # ---------------------
        # BACKUP REMOTE ENVIRONMENT
        # ---------------------

        volume_backup_remote['qos_adaptive_policy_group'] = {}
        volume_backup_remote['qos_adaptive_policy_group']["name"] = f"{svm_backup_remote['name']}_QOP_CLASS_{volume_performace_class}"
        volume_backup_remote['export_policy'] = export_policy_backup_remote
        volume_backup_remote['junction_path'] = junction_path

        # set snapshot policy to none
        log("Setting snapshot policy to none for backup_remote")
        volume_backup_remote['snapshot_policy'] = {}
        volume_backup_remote['snapshot_policy']["name"] = "none"

        # prep backup_remote to create volume, export policy
        backup_remote["volume"] = volume_backup_remote
        backup_remote["export_policy"] = export_policy_backup_remote

        # volume_dr is a string flag '0', '1', '2', '9'
        # 0 = no DR, 1 = DR, 2 = DR and ADPE, 9 = ADPE (no DR)

        # set snapmirror policy and schedule
        if volume_dr == '1' or volume_dr == '2':
            snapmirror_backup_remote["policy"] = f"{snapmirror_policy}TESTDR"
            snapmirror_backup_remote["schedule"] = "hourly_vault"
        else: # volume_dr == '0' or volume_dr == '9'
            snapmirror_backup_remote["policy"] = f"{snapmirror_policy}"
            snapmirror_backup_remote["schedule"] = "daily_vault"
        
        # set destination for snapmirror
        snapmirror_backup_remote["destination"]["svm"]["name"] = svm_backup_remote["name"]
        snapmirror_backup_remote["destination"]["volume"]["name"] = volume_backup_remote["name"]

        backup_remote["snapmirror"] = snapmirror_backup_remote                 

        # ---------------------
        # ADPE ENVIRONMENT
        # ---------------------

        volume_adpe['qos_adaptive_policy_group'] = {}
        volume_adpe['qos_adaptive_policy_group']["name"] = f"{svm_adpe['name']}_QOP_CLASS_{volume_performace_class}"
        volume_adpe['export_policy'] = export_policy_backup_remote
        volume_adpe['junction_path'] = junction_path

        # set snapshot policy to none
        log("Setting snapshot policy to none for adpe")
        volume_adpe['snapshot_policy'] = {}
        volume_adpe['snapshot_policy']["name"] = "none"

        # prep backup_remote to create volume, export policy
        adpe["volume"] = volume_adpe
        adpe["export_policy"] = export_policy_adpe

        # volume_dr is a string flag '0', '1', '2', '9'
        # 0 = no DR, 1 = DR, 2 = DR and ADPE, 9 = ADPE (no DR)

        # set snapmirror policy and schedule
        snapmirror_adpe["policy"] = "VP_30"
        snapmirror_adpe["schedule"] = "ADPE"

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
