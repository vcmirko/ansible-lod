#!/usr/bin/python

# Copyright: (c) 2023, Mirko Van Colen <mirko@netapp.com>
# ==============================================================================
# DESCRIPTION
# A custom module to put an ontap cluster in/out maintenance mode in AIQUM
#
# VERSION HISTORY
# 2023-02-03 - Mirko Van Colen - Initial version
# ==============================================================================
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
import requests         # for rest
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta
from dateutil import parser
from requests.packages.urllib3.exceptions import InsecureRequestWarning # ignore certs
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

summary=[]
hostname=""
username=""
password=""
https=True
validate_certs=False

# add to summary log (verbose output)
def log(t):
    summary.append(t)

# basic auth
def get_auth():
    return HTTPBasicAuth(username,password)

# base uri
def get_base_uri():
    return "{}://{}".format("https" if https else "http",hostname)

# build uri
def get_uri(command=""):
    return "{}{}".format(get_base_uri(),command)

# rest patch
def patch_rest(command,body):
    url=get_uri(command)
    try:
        log("PATCH REST: {}".format(url))
        response = requests.patch(url,auth=get_auth(),json=body,verify=validate_certs)
        log(response.json())
        try:
            if(response.json()['message']):
                print(response.json()['message'])
        except:
            pass        
        response.raise_for_status()
        result = response.json()
        return result
    except requests.exceptions.HTTPError as err:
        raise Exception(err)   

# rest post
def post_rest(command,body):
    url=get_uri(command)
    try:
        log("POST REST: {}".format(url))
        response = requests.post(url,auth=get_auth(),json=body,verify=validate_certs)
        # log(response.json())
        try:
            if(response.json()['message']):
                print(response.json()['message'])
        except:
            pass        
        response.raise_for_status()
        result = response.json()
        return result
    except requests.exceptions.HTTPError as err:
        raise Exception(err)   

# rest post
def put_rest(command,body):
    url=get_uri(command)
    try:
        log("PUT REST: {}".format(url))
        response = requests.put(url,auth=get_auth(),json=body,verify=validate_certs)
        # log(response.json())
        try:
            if(response.json()['message']):
                print(response.json()['message'])
        except:
            pass        
        response.raise_for_status()
        # result = response.json()
        # return result
        return None
    except requests.exceptions.HTTPError as err:
        raise Exception(err)   

# rest get
def get_rest(command):
    url=get_uri(command)
    try:
        log("GET REST: {}".format(url))
        response = requests.get(url,auth=get_auth(),verify=validate_certs)
        # log(response.json())
        try:
            if(response.json()['message']):
                print(response.json()['message'])
        except:
            pass        
        response.raise_for_status()
        result = response.json()
        return result
    except requests.exceptions.HTTPError as err:
        raise Exception(err)   
    
# rest delete
def delete_rest(command):
    url=get_uri(command)
    try:
        log("POST REST: {}".format(url))
        response = requests.delete(url,auth=get_auth(),verify=validate_certs)
        try:
            if(response.json()['message']):
                print(response.json()['message'])
        except:
            pass        
        response.raise_for_status()
        result = response.json()
        return result
    except requests.exceptions.HTTPError as err:
        raise Exception(err)          
    
# get clusters
def get_clusters():
    return (get_rest("/api/v2/admin/datasources/clusters")["records"])

# get cluster
def get_cluster(cluster_name):
    return next((cluster for cluster in get_clusters() if cluster["name"] == cluster_name), None)

# set svm certificate
def start_maintenance(cluster_name, hours):
    cluster = get_cluster(cluster_name)
    if not cluster:
        return None

    log("{} -> starting maintenance for {} hours".format(cluster_name, hours))
    id = cluster["id"]
    current_time = datetime.now()
    start_time = current_time.strftime("%Y-%m-%dT%H:%M:%S%z")
    end_time = (current_time + timedelta(hours=hours)).strftime("%Y-%m-%dT%H:%M:%S%z")
    log("start_time: {}".format(start_time))
    log("end_time: {}".format(end_time))
    body = {
        "datasourceId": id,
        "startTime": start_time,
        "endTime": end_time,
    }
    return post_rest(f"/api/management-server/admin/datasources/{id}/maintenance-windows", body)


def end_maintenance(cluster_name):

    import time

    # start loop, remove all maintenance windows
    done = False
    while not done:

        time.sleep(5)

        cluster = get_cluster(cluster_name)
        
        if not cluster:
            return None

        maintenance_window = cluster.get("maintenance_window")
        
        if not maintenance_window:
            done = True

        else:

            log("{} -> ending maintenance".format(cluster_name))
            id = cluster["id"]
            maintenance_id = maintenance_window["id"]
            current_time = datetime.now()
            start_time = end_time = current_time.strftime("%Y-%m-%dT%H:%M:%S%z")
            log("start_time: {}".format(start_time))
            log("end_time: {}".format(end_time))
            body = {
                "datasourceId": id,
                "startTime": start_time,
                "endTime": end_time,
                "windowId": maintenance_id,
            }
            
            result = put_rest(f"/api/management-server/admin/datasources/{id}/maintenance-windows/{maintenance_id}", body)
            log(result)

    # return last result
    return result

# main code
def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        cluster_name=dict(type='str', required=True),
        hostname=dict(type='str', required=True),
        username=dict(type='str', required=True),
        password=dict(type='str', required=True, no_log=True),
        hours=dict(type='int', required=False, default=3),
        debug=dict(type='bool', required=False, default=False),
        https=dict(type='bool', required=False, default=True),
        validate_certs=dict(type='bool', required=False, default=False),   
        state=dict(type='str', choices=['present', 'absent'], required=True)
    )

    # seed the result dict in the result object
    result = dict(
        changed=False
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    # this is a readonly module, so we didn't implement
    # if module.check_mode:
    #     module.exit_json(**result)

    # store input to vars
    global hostname
    global username
    global password
    global https
    global validate_certs

    hostname=module.params["hostname"]
    username=module.params["username"]
    password=module.params["password"]
    https=module.params["https"]
    debug=module.params["debug"]
    validate_certs=module.params["validate_certs"]
    cluster_name=module.params["cluster_name"]
    hours=module.params["hours"]
    state=module.params["state"]

    err= None
    output=None    


    try:
        if state=="present":
            output = start_maintenance(cluster_name,hours)

        if state=="absent":
            output = end_maintenance(cluster_name)

        # return the result
        result["data"] = output
    except Exception as e:
        log(repr(e))
        err = str(e)

    # build result object
    if(module._verbosity >= 3 or debug==True):
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
