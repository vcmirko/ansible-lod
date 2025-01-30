# Description: Custom Jinja2 filter for Netapp ontap specific tasks

class FilterModule(object):

    
    def filters(self):
        return {
            'auth_pw':self.auth_rest,
            'auth_cert':self.auth_cert,
            'auth_rest':self.auth_rest,
            'keep_deleted_export_policy_rules':self.keep_deleted_export_policy_rules
        }
    
    def auth_rest(self,hostname,username,password="",cert_base="",use_cert=False,https=True,validate_certs=False):
        if not cert_base and not password:
            raise ValueError("Either password or cert_base must be provided")
        if use_cert:
            key_filepath = f"{cert_base}.key"
            cert_filepath = f"{cert_base}.crt"
            return self.auth_cert(hostname,key_filepath,cert_filepath,https,validate_certs)
        else:
            return self.auth_pw(hostname,username,password,https,validate_certs)

    def auth_pw(self,hostname,username,password,https=True,validate_certs=False):
        # return a dictionary with the authentication headers
        return {
            "hostname":hostname,
            "username":username,
            "password":password,
            "https":https,
            "validate_certs":validate_certs
        }

    def auth_cert(self,hostname,key_filepath,cert_filepath,https=True,validate_certs=False):
        # return a dictionary with the authentication headers
        return {
            "hostname":hostname,
            "key_filepath":key_filepath,
            "cert_filepath":cert_filepath,
            "https":https,
            "validate_certs":validate_certs
        }


    def keep_deleted_export_policy_rules(self, rules=[]):
        # only keep items that have is_deleted_item set to True or have state set to absent
        rules_to_delete = [rule for rule in rules if rule.get("is_deleted_item",False) or rule.get("state","") == "absent"]
        # next filter more : if property force_delete_on_first_match is set to True OR rule_index (= number) exists as a property ("rule_index" in rule)
        rules_to_delete = [rule for rule in rules_to_delete if rule.get("force_delete_on_first_match",False) or ("rule_index" in rule)]
        return rules_to_delete