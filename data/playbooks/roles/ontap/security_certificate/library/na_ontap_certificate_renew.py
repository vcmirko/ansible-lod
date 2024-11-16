#!/usr/bin/python

# Copyright: (c) 2023, Mirko Van Colen <mirko@netapp.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
import requests         # for rest
from requests.auth import HTTPBasicAuth
from datetime import datetime
from dateutil import parser
from requests.packages.urllib3.exceptions import InsecureRequestWarning # ignore certs
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

summary=[]
hostname=""
username=""
password=""
key_filepath=""
cert_filepath=""
https=True
validate_certs=False

# add to summary log (verbose output)
def log(t):
    summary.append(t)

# base uri
def get_base_uri():
    return "{}://{}".format("https" if https else "http",hostname)

# build uri
def get_uri(command=""):
    return "{}/api/{}".format(get_base_uri(),command)

# rest patch
def patch_rest(command,body):
    url=get_uri(command)
    try:
        log("PATCH REST: {}".format(url))
        if(username and password):
            response = requests.patch(url,auth=(username,password),json=body,verify=validate_certs)
        else:
            response = requests.patch(url,cert=(cert_filepath, key_filepath),json=body,verify=validate_certs)
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
        if(username and password):
            response = requests.post(url,auth=(username,password),json=body,verify=validate_certs)
        else:
            response = requests.post(url,cert=(cert_filepath, key_filepath),json=body,verify=validate_certs)        
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

# rest get
def get_rest(command):
    url=get_uri(command)
    try:
        log("GET REST: {}".format(url))
        if(username and password):
            response = requests.get(url,auth=(username,password),verify=validate_certs)
        else:
            response = requests.get(url,cert=(cert_filepath, key_filepath),verify=validate_certs)        
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
        log("DELETE REST: {}".format(url))
        if(username and password):
            response = requests.delete(url,auth=(username,password),verify=validate_certs)
        else:
            response = requests.delete(url,cert=(cert_filepath, key_filepath),verify=validate_certs)    
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
    
# get certificates
def get_certs(svm):
    certs = get_rest("security/certificates?fields=expiry_time,svm&type=server".format(svm))
    records = certs.get('records',[])
    cluster_certs = [c for c in records if 'svm' not in c]
    svm_certs = [c for c in records if 'svm' in c and c['svm'].get('name') == svm]
    if svm:
        log(f"Return certs for svm {svm}")
        return svm_certs
    else:
        log(f"Return certs for admin svm")
        return cluster_certs

# get svms
def get_svm(svm):
    svms=get_rest("svm/svms?name={}".format(svm))
    records = svms.get('records',[])
    if len(records)>0:
        return records[0]
    else:
        return {}

# get svms
def get_cluster():
    cluster=get_rest("cluster")
    return cluster  

# set svm certificate
def set_certificate(svm_uuid,certificate_uuid):
    body={}
    body["certificate"]={}
    body["certificate"]["uuid"]=certificate_uuid
    if svm_uuid:
        return patch_rest("svm/svms/{}".format(svm_uuid),body)
    else:
        return patch_rest("cluster",body)

# delete certificate
def delete_cert(certificate):
    log(f"deleting certificate {certificate['name']}")    
    return delete_rest("security/certificates/{}".format(certificate["uuid"]))

# create certificate
def create_cert(svm,days):
    log(f"Creating new certificate with validity of {days} days")
    body={}
    body["type"]="server"
    if svm:
        body["common_name"]=svm           
        body["svm.name"]=svm
    else:
        cluster=get_cluster()
        body["common_name"]=cluster["name"]
    body["expiry_time"]="P{}DT".format(days)
    return post_rest("security/certificates",body)

# register certificate
def register_cert(svm,certificate):
    if svm:
        log(f"registering certificate {certificate['name']} for {svm}")
        svm_o=get_svm(svm)
        set_certificate(svm_o["uuid"],certificate["uuid"])
    else:
        log(f"registering certificate {certificate['name']} for admin svm")
        set_certificate(None,certificate["uuid"])

def get_days_till_eol(certificate):
    now=datetime.now()
    expiry_date=parser.parse(certificate["expiry_time"]).replace(tzinfo=None) 
    return (expiry_date-now).days # remaining days

# main code
def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        svm            = dict(type='str', required=False, default=''),
        hostname       = dict(type='str', required=True),
        username       = dict(type='str', required=False, default=''),
        password       = dict(type='str', required=False, default='', no_log=True),
        key_filepath   = dict(type='str', required=False, default=''),
        cert_filepath  = dict(type='str', required=False, default=''),
        https          = dict(type='bool', required=False, default=True),
        validate_certs = dict(type='bool', required=False, default=False),
        use_rest       = dict(type='bool', required=False, default=False),
        expiry_days    = dict(type='int', required=False, default=365),
        days           = dict(type='int', required=False, default=3650),
        debug          = dict(type='bool', required=False, default=False)
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
    global key_filepath
    global cert_filepath
    global https
    global validate_certs

    hostname=module.params["hostname"]
    username=module.params["username"]
    password=module.params["password"]
    key_filepath=module.params["key_filepath"]
    cert_filepath=module.params["cert_filepath"]
    https=module.params["https"]
    debug=module.params["debug"]
    debug=True
    validate_certs=module.params["validate_certs"]
    svm=module.params["svm"]
    days=module.params["days"]
    expiry_days=module.params["expiry_days"]

    err= None
    output=None    
    certs=[]
    best_cert=None
    certificate_created=False

    # we must authenticate with either username and password or key and cert
    if not (username and password) and not (key_filepath and cert_filepath):
        raise AttributeError("Either username and password or key and cert must be provided")

    try:
        # get certs
        certs = get_certs(svm)

        # if no certificate 
        if len(certs)==0:
            log("No certificate present, we create one")
            create_cert(svm,days)
            certificate_created=True
            certs = get_certs(svm)
        # if all are expired
        elif sum(1 for cert in certs if get_days_till_eol(cert) < expiry_days)==len(certs):
            log("All certificates are expired, we create a new one")
            create_cert(svm,days)
            certificate_created=True
            certs = get_certs(svm)
        else:
            log("Valid certificates found")

        # in case there were more certificates, let's get the best one and set it to svm (if new one, it will be that one)
        if len(certs) > 1:
            log("Found more than 1 certificate, getting the most recent one")
            best_cert = max(certs, key=lambda x: get_days_till_eol(x))
        else:
            log("Found just 1 certificate")
            best_cert = certs[0]  
            log(f"Valid for {get_days_till_eol(best_cert)} days")
        
        # we set the best certificate to the svm
        register_cert(svm,best_cert)  

        # Remove all except the best certificate
        for cert in certs:
            if cert != best_cert:
                delete_cert(cert)

        if certificate_created:
            result["changed"] = True 

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
