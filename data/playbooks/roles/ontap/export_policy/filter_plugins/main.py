# ==============================================================================
# DESCRIPTION
# Filter export policy rules and apply the correct state to each rule (present or absent)
#
# VERSION HISTORY
# 2025-02-03 - Mirko Van Colen - Initial version
# ==============================================================================

class FilterModule(object):

    
    def filters(self):
        return {
            'filter_export_policy_rules':self.filter_export_policy_rules
        }
    
    # Filter export policy rules and apply the correct state to each rule (present or absent)
    def filter_export_policy_rules(self, rules=[]):
        # a deleted rule is a rule that is not new and has state absent or is a deleted item
        # and has a rule_index or force_delete_on_first_match
        rules_to_keep = []
        for rule in rules:
            # we can't have a rule that is both new and deleted => raise an error
            if rule.get('is_deleted_item',False) and rule.get('is_new_item',False):
                raise ValueError("Rule can't be both deleted and new")
            # if the rule is a deleted item or has state absent, we set the state to absent
            if rule.get('is_deleted_item',False) or rule.get('state','') == 'absent':
                rule["state"] = "absent"
                rules_to_keep.append(rule)
                continue
            # if the rule is a new item, or state is present or not set
            if rule.get('is_new_item',False) or rule.get('state','present') == 'present':
                rule["state"] = "present"
                rules_to_keep.append(rule)
                continue

        return rules_to_keep

