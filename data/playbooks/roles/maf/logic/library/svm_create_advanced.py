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

    location       = meta.get("location", "")
    environment    = meta.get("environment", "")
    service        = meta.get("service", "")
    service_level  = meta.get("service_level", "")
    is_dr          = meta.get("is_dr", False)
    resource       = meta.get("resource", "")
    change_request = meta.get("change_request", "")
    customer       = meta.get("customer", "")

    source         = ve.get("source", {})
    destination    = ve.get("destination", {})

    # volumes        = ve.get("volumes", [])

     # apply logic
    try:

        # template
        source["template"] = f"{service}_{service_level}"
        destination["template"] = "svm_dr"



        # create cluster peer object
        cluster_peer = []
        source_cluster = source["cluster"]

        # in lod, we can calculate the intercluster ips, based on the management ip
        # it's a bit of a hack, but it works.  We could have also looked them up by rest api
        source_cluster["intercluster_ips"] = source["cluster"]["management_ip"].replace(".101", ".121").replace(".102", ".123")
        cluster_peer.append(source_cluster)
        destination_cluster = destination["cluster"]
        destination_cluster["intercluster_ips"] = destination.get("cluster", {}).get("management_ip", "").replace(".101", ".121").replace(".102", ".123")
        cluster_peer.append(destination_cluster)

        # complete svm lifs
        source_svm = source["svm"]     
        if source_svm.get("lifs", None):   
            source_svm["lifs"][0]["node"] = f"{source_cluster['name']}-01" # set node name

        # complete volumes
        source_volumes = source.get("volumes", [])
        # loop over volumes
        for volume in source_volumes:
            volume["junction_path"] = f"/{volume['name']}"

        # set destination svm
        destination_svm = {
            "name" : f"{source_svm['name']}_dr"
        }
        destination["svm"] = destination_svm    

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
                "name": destination_cluster["name"],
                "management_ip": destination_cluster["management_ip"]
            },
            "svm": {
                "name": destination_svm["name"]
            }
        }
        vserver_peer.append(peer_source_svm)
        vserver_peer.append(peer_destination_svm)

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
                    "name": destination_cluster["name"],
                    "management_ip": destination_cluster["management_ip"]
                },
            },
            "identity_preserve": "full"
        }

        # set cifs if required
        if service == "SMB":
            ["source"]["cifs"] = {}
            ["source"]["cifs"]["name"] = source_svm["name"].replace("_smb_","").replace("_","")


        # set clusters (for delete)
        clusters = []
        clusters.append(source_cluster)
        clusters.append(destination_cluster)

        source["clusters"] = clusters
        destination["clusters"] = clusters
        ve["snapmirror"] = snapmirror
        ve["vserver_peer"] = vserver_peer
        ve["cluster_peer"] = cluster_peer     

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
