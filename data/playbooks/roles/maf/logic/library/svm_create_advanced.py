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

    location       = meta.get("location", "").lower()
    environment    = meta.get("environment", "").lower()
    service        = meta.get("service", "").lower()
    service_level  = meta.get("service_level", "")
    is_dr          = meta.get("is_dr", False)
    change_request = meta.get("change_request", "")
    customer       = meta.get("customer", "").lower()

    source         = ve.get("source", {})
    destination    = ve.get("destination", {})

    # volumes        = ve.get("volumes", [])

     # apply logic
    try:

        # template
        log("Set templates")
        source["template"] = f"{service}_{service_level}"
        destination["template"] = "svm_dr"



        # create cluster peer object
        cluster_peer = []
        source_cluster = source["cluster"]

        log("Set intercluster ips")
        # in lod, we can calculate the intercluster ips, based on the management ip
        # it's a bit of a hack, but it works.  We could have also looked them up by rest api
        source_cluster["intercluster_ips"] = source["cluster"]["management_ip"].replace(".101", ".121").replace(".102", ".123")
        cluster_peer.append(source_cluster)
        destination_cluster = destination.get("cluster", {})
        destination_cluster["intercluster_ips"] = destination.get("cluster", {}).get("management_ip", "").replace(".101", ".121").replace(".102", ".123")
        cluster_peer.append(destination_cluster)

        log("Set lifs")
        # complete svm lifs
        source_svm = source["svm"]     
        if source_svm.get("lifs", None):   
            source_svm["lifs"][0]["node"] = f"{source_cluster['name']}-01" # set node name

        log("Set junction paths if volumes are given")
        # complete volumes
        source_volumes = source.get("volumes", [])
        # loop over volumes
        for volume in source_volumes:
            volume["junction_path"] = f"/{volume['name']}"

        log("Set destination svm")
        # set destination svm
        destination_svm = {
            "name" : f"{source_svm['name']}_dr"
        }
        destination["svm"] = destination_svm    

        log("Set vserver peer")
        # vserver peer
        vserver_peer = []
        peer_source_svm = {
            "cluster": {
                "name": source_cluster["name"],
                "management_ip": source_cluster["management_ip"]
            },
            "svm": {
                "name": source_svm["name"]
            }
        }
        peer_destination_svm = {
            "cluster": {
                "name": destination_cluster.get("name", ""),
                "management_ip": destination_cluster.get("management_ip", "")
            },
            "svm": {
                "name": destination_svm["name"]
            }
        }
        vserver_peer.append(peer_source_svm)
        vserver_peer.append(peer_destination_svm)

        log("Set snapmirror")
        # set snapmirror
        snapmirror = {
            "source": {
                "svm": {
                    "name": source_svm["name"]
                },
                "cluster": {
                    "name": source_cluster["name"],
                    "management_ip": source_cluster["management_ip"]
                },
            },
            "destination": {
                "svm": {
                    "name": destination_svm["name"]
                },
                "cluster": {
                    "name": destination_cluster.get("name", ""),
                    "management_ip": destination_cluster.get("management_ip", "")
                },
            },
            "identity_preserve": "full"
        }

        log("Set cifs server")
        # set cifs if required
        if service == "smb":
            source["cifs"] = {}
            source["cifs"]["name"] = source_svm["name"].replace("_smb_","").replace("_","")

        if service == "nfs":
            # if nfs, add export policy
            source["export_policy"] = {}
            source["export_policy"]["name"] = f"xp_default"
            source["svm"]["root_volume"] = {}
            source["svm"]["root_volume"]["name"] = f"{source_svm['name']}_root"
            source["svm"]["root_volume"]["export_policy"] = source["export_policy"]["name"]
        
            # auto add 0.0.0.0/0 to export policy for readonly
            rule = {}
            rule["client_match"] = "0.0.0.0/0"
            rule["ro_rule"] = "sys"
            rule["rw_rule"] = "never"
            rule["super_user_security"] = "none"
            source["export_policy"]["rules"] = []
            source["export_policy"]["rules"].append(rule)

        log("Assign everything to the vars_external dict")
        # set clusters (for delete)
        clusters = []
        clusters.append(source_cluster)
        clusters.append(destination_cluster)

        source["clusters"] = clusters
        destination["clusters"] = clusters
        ve["snapmirror"] = snapmirror
        ve["vserver_peer"] = vserver_peer
        ve["cluster_peer"] = cluster_peer     

        log("Drop dr related stuff if not is_dr")
        # now we check if is_dr is set, if not, we remove all dr-related stuff
        if not is_dr:
            # remove dr related stuff
            ve.pop("snapmirror", None)
            ve.pop("vserver_peer", None)
            ve.pop("cluster_peer", None)
            ve.pop("destination", None)

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
