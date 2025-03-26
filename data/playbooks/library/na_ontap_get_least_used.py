#!/usr/bin/python

# Copyright: (c) 2020, Mirko Van Colen <mirko@netapp.com>
# ==============================================================================
# DESCRIPTION
# Returns the best aggregate to place a volume on, based on the available space, used space, provisioned space and volume count.
#
# VERSION HISTORY
# 2025-02-03 - Mirko Van Colen - Initial version
# ==============================================================================
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
import re
# import datetime  # Import the datetime module
import requests
import sys
import urllib3

# Disable SSL certificate warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

summary=[]
message=[]

# Get resource using REST API
def get_resources_rest(cluster_mgmt_ip, username, password, key_filepath, cert_filepath, api, fields, maxRecords=5000):
    url = f"https://{cluster_mgmt_ip}/api/{api}?fields={fields}&maxRecords={maxRecords}"
    # log(f"GET {url}")
    if(username and password):
        response = requests.get(url, auth=(username, password), verify=False)
    else:
        response = requests.get(url, cert=(cert_filepath,key_filepath), verify=False)
    response_json = response.json()
    # log(f"RESPONSE {response_json}")
    return response_json.get("records", [])

# logging 
def log(t):
    global summary
    summary.append(t)


# filter by name and node using includes and excludes
def filter_data_list(data_list, exclude_name_regex="", include_name_regex="",
                     exclude_node_regex="", include_node_regex="",
                     names_to_exclude=[], nodes_to_exclude=[]):

    filtered_data_list = []
    for item in data_list:
        if (not exclude_name_regex or not re.match(exclude_name_regex, item["name"])) and \
                (not include_name_regex or re.match(include_name_regex, item["name"])) and \
                (not exclude_node_regex or not re.match(exclude_node_regex, item["node"])) and \
                (not include_node_regex or re.match(include_node_regex, item["node"])) and \
                item["name"] not in names_to_exclude and item["node"] not in nodes_to_exclude:
            filtered_data_list.append(item)
        else:
            log("Excluded aggregate '{}' on node '{}'".format(item["name"],item["node"]))

    return filtered_data_list

# main code
def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        hostname                  = dict(type='str', required=True),
        username                  = dict(type='str', required=False, default=''),
        password                  = dict(type='str', required=False, default='', no_log=True),
        key_filepath              = dict(type='str', required=False, default=''),
        cert_filepath             = dict(type='str', required=False, default=''),
        debug                     = dict(type='bool', required=False, default=False),
        https                     = dict(type='bool', required=False), # just in case you pass https
        validate_certs            = dict(type='bool', required=False), # just in case you pass validate_certs
        use_rest                  = dict(type='str', required=False), # just in case you pass use_rest
        resource_name             = dict(type='str', required=True),
        resource_api              = dict(type='str', required=True),
        resource_fields           = dict(type='str', required=True),
        resource_name_property    = dict(type='str', required=False, default='name'),
        exclude_name_regex        = dict(type='str', required=False, default=''),
        include_name_regex        = dict(type='str', required=False, default=''),
        names_to_exclude          = dict(type='str', required=False, default=[]),
    )

    # seed the result dict in the result object
    result = dict(
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # store input to vars, some are global
    global summary
    global message
    err = None
    aggregates=[]
    best_candidate = None    
    hostname                  = module.params['hostname']
    username                  = module.params['username']
    password                  = module.params['password']
    key_filepath              = module.params['key_filepath']
    cert_filepath             = module.params['cert_filepath']
    debug                     = module.params['debug']
    resource_name             = module.params['resource_name']
    resource_api              = module.params['resource_api']
    resource_fields           = module.params['resource_fields']
    resource_name_property    = module.params['resource_name_property']
    exclude_name_regex        = module.params['exclude_name_regex']
    include_name_regex        = module.params['include_name_regex']
    names_to_exclude          = module.params['names_to_exclude']


    # we must authenticate with either username and password or key and cert
    if not (username and password) and not (key_filepath and cert_filepath):
        raise AttributeError("Either username and password or key and cert must be provided")

    try:

        # check mutually exclusive parameters
        if(exclude_name_regex and include_name_regex):
            raise AttributeError("'exclude_name_regex' and 'include_name_regex' are mutually exclusive")
        if(exclude_name_regex and names_to_exclude):
            raise AttributeError("'exclude_name_regex' and 'names_to_exclude' are mutually exclusive")
        


        # get all aggregates
        aggregates = get_aggregates(hostname, username, password, key_filepath, cert_filepath, requested_size_mb, 1, volume_name, svm_name)
        result["all_aggregates"] = aggregates
        print(*message, file=sys.stdout)

        # only filter if volume not already exists
        global volume_exists
        if not volume_exists:
            # filter by external filters (regex & lists)
            # log(f"Filtering with : exclude_name_regex={exclude_name_regex}, include_name_regex={include_name_regex}, exclude_node_regex={exclude_node_regex}, include_node_regex={include_node_regex}, names_to_exclude={names_to_exclude}, nodes_to_exclude={nodes_to_exclude}")

            aggregates = filter_data_list(aggregates, exclude_name_regex, include_name_regex,
                                                exclude_node_regex, include_node_regex,
                                                names_to_exclude, nodes_to_exclude)
            
            # rank them and sort by rank
            aggregates = rank_normalize_sort(aggregates, properties_to_rank, weights, thresholds, sort_orders)
        else:
            pass
        # we now have all the valid candidates
        result["valid_candidates"] = aggregates

        # get best result
        if aggregates:    
            best_candidate = aggregates[0]
            log("aggregate '{}' is our best choice".format(best_candidate["name"]))  
            log("scores : ")      
            for item in aggregates:
                log("- {} -> {}".format(item["name"],item["final_score"]))
            result["aggregate"]=best_candidate
        else:
            raise LookupError("No suitable aggregates found\n\n{}")

    except Exception as e:
        log(repr(e))
        err = str(e)

    # build result object
    # if(module._verbosity >= 3 or debug==True):
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
