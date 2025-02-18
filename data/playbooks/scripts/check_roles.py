# go into the roles folder
# every subfolder is a collection of roles
# and every subfolder in a collection is a role
# under tasks of every role there are yml files
# I have a special structure 
# => main.yml is a proxy for the role, I always run roles with a qtask variable
# => the qtask is the actual task that needs to be run
# => let's start with writing a readme file for every role, overwriting the existing one if needed
# => the readme file should contain a 

import os
import yaml
import jinja2
import re
import time
from termcolor import colored

roles_to_skip = []
collections_to_skip = ["role_template"]
qtasks_to_skip = ["main.yml", "facts.yml",".*_one.yml$",".*_multi.yml$","^facts_.*","^_.*"]
tasks_to_skip = ["Set authentication facts","Logging","Set facts"]
task_parts_to_drop = [r"\[.*\]"]
templates_path = '../templates'
roles_path = '../roles'

# set the path to the script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def template_to_file(template, file, vars, check=False):
    if check and os.path.exists(file):
        return
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(f"{templates_path}/"))
    template = env.get_template(template)
    output = template.render(vars)
    output = output.replace("{|{","{{")
    output = output.replace("}|}","}}")    
    print(f"... Creating file {file}")
    with open(file, 'w') as f:
        f.write(output)    

def add_file_property(file, property, value):
    with open(file) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        if not data:
            return

        properties = property.split('.')
        current = data
        for i in range(len(properties)):
            if i == len(properties) - 1:
                # last property
                if properties[i] not in current:
                    current[properties[i]] = value
                    print(colored(f"Adding property {property} with value {value} to file {file}", "cyan"))
                    with open(file, 'w') as f:
                        yaml.dump(data, f, default_flow_style=False)
                else:
                    pass
                    # property already exists
            else:
                if properties[i] not in current:
                    current[properties[i]] = {}
                current = current[properties[i]]

def drop_multi_regex(t,list):
    result = t
    for regex in list:
        # remove all occurences of the regex
        result = re.sub(regex, '', result)
    return result

def check_multi_regex(t,list):
    for regex in list:
        if re.match(regex, t):
            return True
    return False

def check_roles():
    collections = os.listdir(roles_path)
    # collections = ontap, ...
    for collection in collections:
        if not os.path.isdir(f'{roles_path}/{collection}'):
            continue

        if collection in collections_to_skip:
            continue

        print(colored(f"Checking collection {collection}", "blue", attrs=["bold"]))

        roles = os.listdir(f'{roles_path}/{collection}')
        # roles = svm, volume, ...

        for role_name in roles:

            if role_name in roles_to_skip:
                continue

            role = {}
            role["name"] = role_name
            role["qtasks"] = []

            if os.path.isdir(f'{roles_path}/{collection}/{role_name}'):
                # check if the role has a tasks folder

                if not os.path.exists(f'{roles_path}/{collection}/{role_name}/tasks'):
                    continue

                # print a subheader
                print(colored(f"Checking role {role_name}", "green"))

                # check if the role has a meta folder with main.yml file
                os.makedirs(f'{roles_path}/{collection}/{role_name}/meta', exist_ok=True)

                template_to_file(
                    'role_meta_meta.yml.j2',
                    f'{roles_path}/{collection}/{role_name}/meta/meta.yml',
                    {},
                    True
                )

                # get the role description
                with open(f'{roles_path}/{collection}/{role_name}/meta/meta.yml') as f:
                    meta = yaml.load(f, Loader=yaml.FullLoader)
                    role["description"] = meta['role']['description']
                    role["supports_multi"] = meta["role"].get("supports_multi", False)
                    role["key"] = meta["role"].get("key", "name")

                tasks = os.listdir(f'{roles_path}/{collection}/{role_name}/tasks')
                for qtask in tasks:
                    # continue if the file is not a yml file
                    if not qtask.endswith('.yml'):
                        print(colored(f"Skipping file {qtask} as it is not a yml file", "yellow"))
                        continue

                    if check_multi_regex(qtask, qtasks_to_skip):
                        continue
                   
                    role_qtask = {}
                    role_qtask["name"] = qtask[:-4]

                    # check / create the _one and _multi files

                    if role["supports_multi"]:

                        # create main with loop item
                        template_to_file(
                            'role_main_multi.yml.j2', 
                            f'{roles_path}/{collection}/{role_name}/tasks/main.yml', 
                            {"role": role_name},
                            True
                        )

                        # create facts multi
                        template_to_file(
                            'role_facts_multi.yml.j2',
                            f'{roles_path}/{collection}/{role_name}/tasks/facts_multi.yml',
                            {"collection": collection, "role": role_name, "key": role["key"]},
                            True
                        )

                        # if _one file doesn't contain string "facts.yml", delete the file
                        delete_file = False
                        with open(f'{roles_path}/{collection}/{role_name}/tasks/{role_qtask["name"]}_one.yml') as f:
                            if "facts.yml" not in f.read():
                                print(colored(f"Deleting file {role_qtask['name']}_one.yml", "red"))
                                delete_file = True

                        if delete_file:
                            os.remove(f'{roles_path}/{collection}/{role_name}/tasks/{role_qtask["name"]}_one.yml')
                        

                        # create one file if it does not exist
                        template_to_file(
                            'role_qtask_one.yml.j2',
                            f'{roles_path}/{collection}/{role_name}/tasks/{role_qtask["name"]}_one.yml',
                            {"collection": collection, "role": role_name, "qtask": role_qtask["name"]},
                            True
                        )
                        
                        # create multi file if it does not exist
                        template_to_file(
                            'role_qtask_multi.yml.j2',
                            f'{roles_path}/{collection}/{role_name}/tasks/{role_qtask["name"]}_multi.yml',
                            {"collection": collection, "role": role_name, "qtask": role_qtask["name"], "key": role["key"]},
                            True
                        )

                    else:
                        # create main.yml without loop item
                        template_to_file(
                            'role_main.yml.j2',
                            f'{roles_path}/{collection}/{role_name}/tasks/main.yml',
                            {"role": role_name},
                            True
                        )

 
check_roles() 