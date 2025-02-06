#!/usr/bin/python

# (c) 2019-2025, NetApp, Inc
# ==============================================================================
# DESCRIPTION
# Invoke the ONTAP REST API to run a CLI command but with extended idempotency checks
# Mostly cloned from na_ontap_rest_cli.py
#
# VERSION HISTORY
# 2025-02-03 - Mirko Van Colen - Initial version
# ==============================================================================
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

'''
na_ontap_rest_cli
'''

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
Extended by Mirko Van Colen (cloned from na_ontap_rest_cli.py)
# consolidated required utilities
# added idempotency_params to allow for idempotent check operations

author: NetApp Ansible Team (@carchi8py) <ng-ansibleteam@netapp.com>
description:
  - Run CLI commands on ONTAP through REST api/private/cli/.
  - This module can run as admin or vsdamin and requires HTTP application to be enabled.
  - Access permissions can be customized using ONTAP rest-role.
extends_documentation_fragment:
  - netapp.ontap.netapp.na_ontap_rest
module: na_ontap_rest_cli
short_description: NetApp ONTAP run any CLI command using REST api/private/cli/
version_added: 2.9.0
options:
  command:
    description:
      - A CLI command.
    required: true
    type: str
  verb:
    description:
      - Define which action to perform with the provided command.
      - Values are mapped to show, create, modify, delete.
      - OPTIONS is useful to know which verbs are supported by the REST API
    choices: ['GET', 'POST', 'PATCH', 'DELETE', 'OPTIONS']
    required: true
    type: str
  params:
    description:
      - a dictionary of parameters to pass into the api call
    type: dict
  body:
    description:
      - a dictionary for info specification
    type: dict
  idempotency_params:
    description:
      - a dictionary of parameters to control idempotency checks
    type: dict
    suboptions:
      ignore_failure:
          regex: A regex pattern to match against the error message. If the pattern is found, the error is ignored.
          negate: If true, the regex pattern is negated.
      not_changed:
          regex: A regex pattern to match against the error message. If the pattern is found, the changed flag is set to false.
          negate: If true, the regex pattern is negated.
          num_records: A string with an operator (==, !=, <, <=, >, >=) followed by a number. If the number of records returned by the command matches the operator, the changed flag is set to false.
      custom_messages:
          ignore_failure: A custom message to return if an error is ignored.
          changed: A custom message to return if the changed flag is set to true.
      precheck:
          rest_cli:
              command: The command like /volume/quota/policy
              verb: The verb like GET, POST, PATCH, DELETE, OPTIONS
              params: A dictionary of parameters to pass into the api call
              body: A dictionary for post or patch info specification
          ignore_failure:
              regex: A regex pattern to match against the error message of the precheck. If the pattern is found, the error is ignored.
              negate: If true, the regex pattern is negated.
          skip_main_command:
              error_message:
                  regex: A regex pattern to match against the error message of the precheck. If the pattern is found, the main command is skipped.
                  negate: If true, the regex pattern is negated.
              num_records: A string with an operator (==, !=, <, <=, >, >=) followed by a number. If the number of records returned by the precheck matches the operator, the main command is skipped.
          custom_messages:
              skipped: A custom message to return if the main command is skipped.
'''

EXAMPLES = """
- name: Run ONTAP REST CLI command like the original na_ontap_rest_cli
  na_ontap_rest_cli_idempotent:
    hostname: "{{ netapp_hostname }}"
    username: "{{ netapp_username }}"
    password: "{{ netapp_password }}"
    command: version
    verb: GET

- name: "Create/Modify Quota Policy using REST CLI Idempotent"
  na_ontap_rest_cli_idempotent:
    command: "volume/quota/policy"
    verb: POST
    body: 
        policy_name: "my_quota_policy"
        vserver: "my_svm"
    idempotency_params:
        ignore_failure: 
            regex: "duplicate entry"
        not_changed:
            regex: "duplicate entry"
        custom_messages:
            ignore_failure: "Quota policy already exists"
            changed: "Quota policy created"
    <<: *auth # include authentication parameters
            
- name: "Set Quota Policy as active on SVM using REST CLI Idempotent"
  na_ontap_rest_cli_idempotent:
    command: "vserver"
    verb: PATCH
    body: 
        quota_policy: "my_quota_policy"
    params:
        vserver: "my_svm"
    idempotency_params:
    custom_messages:
        changed: "Quota policy my_quota_policy set as active on SVM my_svm"
    precheck:
        rest_cli:
            command: "vserver"
            verb: GET
            params:
                quota_policy: "my_quota_policy"
                vserver: "my_svm"
        skip_main_command:
            num_records: "==1"   
    <<: *auth # include authentication parameters                        

"""

RETURN = """
"""

import traceback
import time
import logging
import requests
import re

from ansible.module_utils.basic import AnsibleModule

LOG = logging.getLogger(__name__)

def set_auth_method(module, username, password, cert_filepath, key_filepath):
    error = None
    auth_method = None
    if password is None and username is None:
        if cert_filepath is None:
            error = ('Error: cannot have a key file without a cert file' if key_filepath is not None
                     else 'Error: ONTAP module requires username/password or SSL certificate file(s)')
        else:
            auth_method = 'single_cert' if key_filepath is None else 'cert_key'
    elif password is not None and username is not None:
        if cert_filepath is not None or key_filepath is not None:
            error = 'Error: cannot have both basic authentication (username/password) ' +\
                    'and certificate authentication (cert/key files)'
        else:
            auth_method = 'basic_auth' if has_feature(module, 'classic_basic_authorization') else 'speedy_basic_auth'
    else:
        error = 'Error: username and password have to be provided together'
        if cert_filepath is not None or key_filepath is not None:
            error += ' and cannot be used with cert or key files'
    if error:
        module.fail_json(msg=error)
    return auth_method

def has_feature(module, feature_name):
    feature = get_feature(module, feature_name)
    if isinstance(feature, bool):
        return feature
    module.fail_json(msg="Error: expected bool type for feature flag: %s" % feature_name)

def get_feature(module, feature_name):
    ''' if the user has configured the feature, use it
        otherwise, use our default
    '''
    default_flags = dict(
        strict_json_check=True,                 # when true, fail if response.content in not empty and is not valid json
        trace_apis=False,                       # when true, append ZAPI and REST requests/responses to /tmp/ontap_zapi.txt
        trace_headers=False,                    # when true, headers are not redacted in send requests
        trace_auth_args=False,                  # when true, auth_args are not redacted in send requests
        check_required_params_for_none=True,
        classic_basic_authorization=False,      # use ZAPI wrapper to send Authorization header
        deprecation_warning=True,
        sanitize_xml=True,
        sanitize_code_points=[8],               # unicode values, 8 is backspace
        show_modified=True,
        always_wrap_zapi=True,                  # for better error reporting
        flexcache_delete_return_timeout=5,      # ONTAP bug if too big?
        # for SVM, whch protocols can be allowed
        svm_allowable_protocols_rest=['cifs', 'fcp', 'iscsi', 'nvme', 'nfs', 'ndmp', 's3'],
        svm_allowable_protocols_zapi=['cifs', 'fcp', 'iscsi', 'nvme', 'nfs', 'ndmp', 'http'],
        max_files_change_threshold=1,           # percentage of increase/decrease required to trigger a modify action
        warn_or_fail_on_fabricpool_backend_change='fail',
        no_cserver_ems=False                    # when True, don't attempt to find cserver and don't send cserver EMS
    )

    if module.params['feature_flags'] is not None and feature_name in module.params['feature_flags']:
        return module.params['feature_flags'][feature_name]
    if feature_name in default_flags:
        return default_flags[feature_name]
    module.fail_json(msg="Internal error: unexpected feature flag: %s" % feature_name)

def check_regex(error,regex,negate):
    if regex and re.search(regex, error):
        if negate:
            return False
        else:
            return True
    return False

def is_changed_false(text,regex,negate):
    if regex and re.search(regex, text):
        if negate:
            return True
        else:
            return False
    # default to changed
    return True

def check_num_records(result,num_records):
    # if result is dict and has num_records key
    # then compare with num_records
    # num records must be stripped from spaces
    # if should contain an oparator (==, !=, <, <=, >, >=)
    # followed by a number
    if num_records is None:
        return False
    
    num_records = num_records.strip().replace(' ', '')
    if isinstance(result, dict) and 'num_records' in result:
        if num_records:
            num_records = num_records.strip()
            if num_records.startswith('=='):
                return result['num_records'] == int(num_records[2:])
            if num_records.startswith('!='):
                return result['num_records'] != int(num_records[2:])
            if num_records.startswith('<='):
                return result['num_records'] <= int(num_records[2:])
            if num_records.startswith('>='):
                return result['num_records'] >= int(num_records[2:])
            if num_records.startswith('<'):
                return result['num_records'] < int(num_records[1:])
            if num_records.startswith('>'):
                return result['num_records'] > int(num_records[1:])
            else:
                raise ValueError("num_records must be of the format (==, !=, <, <=, >, >=) followed by a number")
    else:
        pass # the result didn't have num_records
    return False

class OntapRestAPI(object):
    ''' wrapper to send requests to ONTAP REST APIs '''
    def __init__(self, module, timeout=60, host_options=None):
        self.host_options = module.params if host_options is None else host_options
        self.module = module
        # either username/password or a certifcate with/without a key are used for authentication
        self.username = self.host_options.get('username')
        self.password = self.host_options.get('password')
        self.hostname = self.host_options['hostname']
        self.use_rest = self.host_options['use_rest'].lower()
        self.cert_filepath = self.host_options.get('cert_filepath')
        self.key_filepath = self.host_options.get('key_filepath')
        self.verify = self.host_options['validate_certs']
        self.timeout = timeout
        port = self.host_options['http_port']
        self.force_ontap_version = self.host_options.get('force_ontap_version')
        if port is None:
            self.url = 'https://%s/api/' % self.hostname
        else:
            self.url = 'https://%s:%d/api/' % (self.hostname, port)
        self.is_rest_error = None
        self.fallback_to_zapi_reason = None
        self.ontap_version = dict(
            full='unknown',
            generation=-1,
            major=-1,
            minor=-1,
            valid=False
        )
        self.errors = []
        self.debug_logs = []
        self.auth_method = set_auth_method(self.module, self.username, self.password, self.cert_filepath, self.key_filepath)


    def log_error(self, status_code, message):
        LOG.error("%s: %s", status_code, message)
        self.errors.append(message)
        self.debug_logs.append((status_code, message))

    def log_debug(self, status_code, content):
        LOG.debug("%s: %s", status_code, content)
        self.debug_logs.append((status_code, content))

    def build_headers(self, accept=None, vserver_name=None, vserver_uuid=None):
        headers = {}
        # accept is used to turn on/off HAL linking
        if accept is not None:
            headers['accept'] = accept
        # vserver tunneling using vserver name and/or UUID
        if vserver_name is not None:
            headers['X-Dot-SVM-Name'] = vserver_name
        if vserver_uuid is not None:
            headers['X-Dot-SVM-UUID'] = vserver_uuid
        return headers

    def send_request(self, method, api, params, json=None, headers=None, files=None):
        ''' send http request and process reponse, including error conditions '''
        url = self.url + api

        def get_auth_args():
            if self.auth_method == 'single_cert':
                kwargs = dict(cert=self.cert_filepath)
            elif self.auth_method == 'cert_key':
                kwargs = dict(cert=(self.cert_filepath, self.key_filepath))
            elif self.auth_method in ('basic_auth', 'speedy_basic_auth'):
                # with requests, there is no challenge, eg no 401.
                kwargs = dict(auth=(self.username, self.password))
            else:
                raise KeyError(self.auth_method)
            return kwargs

        status_code, json_dict, error_details = self._send_request(method, url, params, json, headers, files, get_auth_args())

        return status_code, json_dict, error_details

    def _send_request(self, method, url, params, json, headers, files, auth_args):
        status_code = None
        json_dict = None
        json_error = None
        error_details = None
        if headers is None:
            headers = self.build_headers()

        def fail_on_non_empty_value(response):
            '''json() may fail on an empty value, but it's OK if no response is expected.
               To avoid false positives, only report an issue when we expect to read a value.
               The first get will see it.
            '''
            if method == 'GET' and has_feature(self.module, 'strict_json_check'):
                contents = response.content
                if len(contents) > 0:
                    raise ValueError("Expecting json, got: %s" % contents)

        def get_json(response):
            ''' extract json, and error message if present '''
            try:
                json = response.json()
            except ValueError:
                fail_on_non_empty_value(response)
                return None, None
            return json, json.get('error')

        try:
            response = requests.request(method, url, verify=self.verify, params=params,
                                        timeout=self.timeout, json=json, headers=headers, files=files, **auth_args)
            status_code = response.status_code
            self.log_debug(status_code, response.content)
            # If the response was successful, no Exception will be raised
            response.raise_for_status()
            json_dict, json_error = get_json(response)
        except requests.exceptions.HTTPError as err:
            try:
                __, json_error = get_json(response)
            except (AttributeError, ValueError):
                json_error = None
            if json_error is None:
                self.log_error(status_code, 'HTTP error: %s' % err)
                error_details = str(err)

            # If an error was reported in the json payload, it is handled below
        except requests.exceptions.ConnectionError as err:
            self.log_error(status_code, 'Connection error: %s' % err)
            error_details = str(err)
        except Exception as err:
            self.log_error(status_code, 'Other error: %s' % err)
            error_details = str(err)
        if json_error is not None:
            self.log_error(status_code, 'Endpoint error: %d: %s' % (status_code, json_error))
            error_details = json_error
        if not error_details and not json_dict:
            if json_dict is None:
                json_dict = {}
            if method == 'OPTIONS':
                # OPTIONS provides the list of supported verbs
                json_dict['Allow'] = response.headers.get('Allow')
            if response.headers.get('Content-Type', '').startswith("multipart/form-data"):
                json_dict['text'] = response.text
        return status_code, json_dict, error_details

    def get(self, api, params=None, headers=None):
        method = 'GET'
        dummy, message, error = self.send_request(method, api, params, json=None, headers=headers)
        return message, error

    def post(self, api, body, params=None, headers=None, files=None):
        method = 'POST'
        retry = 3
        while retry > 0:
            dummy, message, error = self.send_request(method, api, params, json=body, headers=headers, files=files)
            if error and isinstance(error, dict) and 'temporarily locked' in error.get('message', ''):
                time.sleep(30)
                retry = retry - 1
                continue
            break
        return message, error

    def patch(self, api, body, params=None, headers=None, files=None):
        method = 'PATCH'
        retry = 3
        while retry > 0:
            dummy, message, error = self.send_request(method, api, params, json=body, headers=headers, files=files)
            if error and isinstance(error, dict) and 'temporarily locked' in error.get('message', ''):
                time.sleep(30)
                retry = retry - 1
                continue
            break
        return message, error

    def delete(self, api, body=None, params=None, headers=None):
        method = 'DELETE'
        dummy, message, error = self.send_request(method, api, params, json=body, headers=headers)
        return message, error

    def options(self, api, params=None, headers=None):
        method = 'OPTIONS'
        dummy, message, error = self.send_request(method, api, params, json=None, headers=headers)
        return message, error

class NetAppONTAPCommandREST():
    ''' calls a CLI command '''

    def __init__(self):
        self.argument_spec = dict(
            hostname=dict(required=True, type='str'),
            username=dict(required=False, type='str', aliases=['user']),
            password=dict(required=False, type='str', aliases=['pass'], no_log=True),
            https=dict(required=False, type='bool', default=False),
            validate_certs=dict(required=False, type='bool', default=True),
            http_port=dict(required=False, type='int'),
            use_rest=dict(required=False, type='str', default='always'),
            feature_flags=dict(required=False, type='dict'),
            cert_filepath=dict(required=False, type='str'),
            key_filepath=dict(required=False, type='str', no_log=False),
            force_ontap_version=dict(required=False, type='str'),
            command=dict(required=True, type='str'),
            verb=dict(required=True, type='str', choices=['GET', 'POST', 'PATCH', 'DELETE', 'OPTIONS']),
            params=dict(required=False, type='dict'),
            body=dict(required=False, type='dict'),
            idempotency_params=dict(required=False, type='dict', default={}),
        )
        self.module = AnsibleModule(
            argument_spec=self.argument_spec,
            supports_check_mode=True
        )
        self.rest_api = OntapRestAPI(self.module)
        parameters = self.module.params
        # set up state variables
        self.command = parameters['command']
        self.verb = parameters['verb']
        self.params = parameters['params']
        self.body = parameters['body']

        self.idempotency_params = parameters.get('idempotency_params', {})
        self.ignore_failure = self.idempotency_params.get('ignore_failure', {})
        self.not_changed = self.idempotency_params.get('not_changed', {})
        self.custom_messages = self.idempotency_params.get('custom_messages', {})

        self.ignore_failure_regex = self.ignore_failure.get('regex', None)
        self.ignore_failure_negate = self.ignore_failure.get('negate', False)

        self.not_changed_regex = self.not_changed.get('regex', None)
        self.not_changed_negate = self.not_changed.get('negate', False)
        self.not_changed_num_records = self.not_changed.get('num_records', None)

        self.custom_message_ignore_failure = self.custom_messages.get('ignore_failure', None)
        self.custom_message_changed = self.custom_messages.get('changed', None)

        self.precheck = self.idempotency_params.get('precheck', {}) 

        self.precheck_rest_cli = self.precheck.get('rest_cli', {})
        self.precheck_rest_cli_command = self.precheck_rest_cli.get('command', None)
        self.precheck_rest_cli_verb = self.precheck_rest_cli.get('verb', None)
        self.precheck_rest_cli_params = self.precheck_rest_cli.get('params', None)
        self.precheck_rest_cli_body = self.precheck_rest_cli.get('body', None)

        self.precheck_ignore_failure = self.precheck.get('ignore_failure', {})
        self.precheck_ignore_failure_message = self.precheck_ignore_failure.get('message', None)
        self.precheck_ignore_failure_regex = self.precheck_ignore_failure.get('regex', None)
        self.precheck_ignore_failure_negate = self.precheck_ignore_failure.get('negate', False)

        self.precheck_skip_main_command = self.precheck.get('skip_main_command', {})
        self.precheck_skip_main_command_error_message = self.precheck_skip_main_command.get('error_message', {})
        self.precheck_skip_main_command_error_regex = self.precheck_skip_main_command_error_message.get('regex', None)
        self.precheck_skip_main_command_error_negate = self.precheck_skip_main_command_error_message.get('negate', False)
        self.precheck_skip_main_command_num_records = self.precheck_skip_main_command.get('num_records', None)
        self.precheck_skip_main_command_error_message = self.precheck_skip_main_command.get('error_message', None)
        
        self.precheck_custom_messages = self.precheck.get('custom_messages', {})    
        self.precheck_custom_message_skipped = self.precheck_custom_messages.get('skipped', None)

        self.use_rest = True
        self.error_occurred = False
        self.is_skipped = False

    def run_command(self):
        api = "private/cli/" + self.command
        precheck_result = None
        pre_error = None
        message = None
        error = None

        # do a idempotency pre check
        if self.precheck_rest_cli_command:
            
            precheck_api = "private/cli/" + self.precheck_rest_cli_command

            if self.precheck_rest_cli_verb == 'POST':
                precheck_result, pre_error = self.rest_api.post(precheck_api, self.precheck_rest_cli_body, self.precheck_rest_cli_params)
            elif self.precheck_rest_cli_verb == 'GET':
                precheck_result, pre_error = self.rest_api.get(precheck_api, self.precheck_rest_cli_params)
            elif self.precheck_rest_cli_verb == 'PATCH':
                precheck_result, pre_error = self.rest_api.patch(precheck_api, self.precheck_rest_cli_body, self.precheck_rest_cli_params)
            elif self.precheck_rest_cli_verb == 'DELETE':
                precheck_result, pre_error = self.rest_api.delete(precheck_api, self.precheck_rest_cli_body, self.precheck_rest_cli_params)
            elif self.precheck_rest_cli_verb == 'OPTIONS':
                precheck_result, pre_error = self.rest_api.options(precheck_api, self.precheck_rest_cli_params)
            else:
                self.module.fail_json(msg='Error: unexpected verb %s' % self.precheck_rest_cli_verb,
                                      exception=traceback.format_exc())
            
        # check if we care about precheck errors
        if pre_error:
            stringError = str(pre_error)
            # do we ignore the error?
            if check_regex(stringError, self.precheck_ignore_failure_regex, self.precheck_ignore_failure_negate):
                if check_regex(stringError, self.precheck_skip_main_command_error_regex, self.precheck_skip_main_command_error_negate):
                    self.is_skipped = True
            else:
                self.module.fail_json(msg='Error in precheck: %s' % pre_error)

        # check if we should skip the main command based on precheck result
        else:
            if precheck_result:
                if check_num_records(precheck_result, self.precheck_skip_main_command_num_records):
                    self.is_skipped = True

        if self.is_skipped:
            return self.precheck_custom_message_skipped or "Skipped due to precheck"

        if self.verb == 'POST':
            message, error = self.rest_api.post(api, self.body, self.params)
        elif self.verb == 'GET':
            message, error = self.rest_api.get(api, self.params)
        elif self.verb == 'PATCH':
            message, error = self.rest_api.patch(api, self.body, self.params)
        elif self.verb == 'DELETE':
            message, error = self.rest_api.delete(api, self.body, self.params)
        elif self.verb == 'OPTIONS':
            message, error = self.rest_api.options(api, self.params)
        else:
            self.module.fail_json(msg='Error: unexpected verb %s' % self.verb,
                                  exception=traceback.format_exc())

        if error:
            self.error_occurred = True
            stringError = str(error)
            # do we ignore the error?
            if check_regex(stringError, self.ignore_failure_regex, self.ignore_failure_negate):
                message = stringError
            else:
                self.module.fail_json(msg='Error: %s' % error)

        return message

    def apply(self):

        ''' calls the command and returns raw output '''
        if self.module.check_mode and self.verb in ['POST', 'PATCH', 'DELETE']:
            output = "Would run command: '%s'" % str(self.command)
        else:
            output = self.run_command()

        changed = True

        if self.is_skipped:
            self.module.exit_json(changed=False, msg=output)

        else:

            # set flag changed to false ?
            if self.verb in ['GET', 'OPTIONS']:
                changed = False
            elif self.error_occurred:
                changed = is_changed_false(output, self.not_changed_regex, self.not_changed_negate)
            else:
                changed = not check_num_records(output, self.not_changed_num_records)

            # in case of error but ignored, add custom message if provided
            if self.error_occurred and self.custom_message_ignore_failure:
                output = self.custom_message_ignore_failure

            if changed and self.custom_message_changed:
                output = self.custom_message_changed
            self.module.exit_json(changed=changed, msg=output)

def main():
    """
    Execute action from playbook
    """
    command = NetAppONTAPCommandREST()
    command.apply()


if __name__ == '__main__':
    main()