import re

# ==============================================================================
# DESCRIPTION
# A library with common functions used for generali
#
# VERSION HISTORY
# 2025-02-03 - Mirko Van Colen - Initial version
# ==============================================================================

def get_resource_name(resource_name, resource_type):
    return re.sub(r"_..$", f"_{resource_type}", resource_name)

def get_admin_acl(country):

    acl = {}
    acl["state"] = "present"
    acl["permission"] = "full_control"
    if country == 'DE':
        acl["user_or_group"] = f"DE\\usrsDE_T01_RLE_STO_AdminsFileShare"
    elif country == 'FR':
        acl["user_or_group"] = f"GROUPE\\usrsFR_T01_RLE_STO_AdminsFileShare"
    elif country == 'IT':
        acl["user_or_group"] = f"CORPGEN\\usrsIT_T01_RLE_STO_AdminsFileShare"
    elif country == 'default':
        acl["user_or_group"] = f"GENERALINET\\usrsZZ_T01_RLE_STO_AdminsFileShare"
    else:
        return None
    return acl

def is_local_backup(service_level, volume_dr):
    return service_level == 'M1' or service_level == 'M2' or service_level == 'S1' or service_level == 'S2' or service_level == 'L1' or service_level == 'R2'

def is_remote_backup(service_level, volume_dr):
    return service_level == 'M2' or service_level == 'S2' or service_level == 'R2'

def is_adpe(service_level, volume_dr):
    return volume_dr == '2' or volume_dr == '9'

def remove_unused_environments(vars_external, service_level, volume_dr):
    if not is_local_backup(service_level, volume_dr):
        vars_external.pop('backup_local')
    if not is_remote_backup(service_level, volume_dr):
        vars_external.pop('backup_remote')
    if not is_adpe(service_level, volume_dr):
        vars_external.pop('adpe')
    return vars_external