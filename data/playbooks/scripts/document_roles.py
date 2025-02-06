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
from termcolor import colored

roles_to_skip = []
collections_to_skip = ["role_template"]
qtasks_to_skip = ["main", "facts",".*_one$",".*_multi$","^facts_.*","^_.*"]
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
    with open(file, 'w') as f:
        f.write(output)    

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

def get_link(name):
    return name.lower().replace(' ', '-').replace('/','')

def document_roles():
    collection_names = os.listdir(roles_path)
    # like ontap, maf, aiqume

    collections = []
    for collection_name in collection_names:

        # must be a directory
        if not os.path.isdir(f'{roles_path}/{collection_name}'):
            continue

        # skip some collections if needed
        if collection_name in collections_to_skip:
            continue

        template_to_file(
            'collection_galaxy.yml.j2',
            f'{roles_path}/{collection_name}/galaxy.yml',
            {"collection_name": collection_name},
            check=True
        )        

        # read the galaxy.yml file
        with open(f'{roles_path}/{collection_name}/galaxy.yml') as f:
            galaxy_data = yaml.load(f, Loader=yaml.FullLoader)

        collection = {}
        collection["name"] = collection_name
        collection["description"] = galaxy_data.get("description", "")
        collection["link"] = get_link(collection_name)
        collection["roles"] = []
        print(colored(f"Collection {collection_name}", 'blue', attrs=['bold']))

        role_names = os.listdir(f'{roles_path}/{collection_name}')
        # svm, volume, ...



        for role_name in role_names:

            if not os.path.isdir(f'{roles_path}/{collection_name}/{role_name}'):
                # check if the role is a directory
                continue

            if role_name in roles_to_skip:
                continue

            print(colored(f"Role {role_name}", 'green'))

            role = {}
            role["name"] = role_name
            role["link"] = get_link(f"{collection_name} / {role_name}")
            role["qtasks"] = []

            if not os.path.exists(f'{roles_path}/{collection_name}/{role_name}/tasks'):
                # print with color
                print(colored(f"Role {role_name} does not have a tasks folder", 'red'))
                continue

            

            # check if the role has a meta folder with main.yml file
            # if it does, extra the role description
            if not os.path.exists(f'{roles_path}/{collection_name}/{role_name}/meta'):
                print(colored(f"Role {role_name} does not have a meta folder", 'yellow'))
                continue

            # get the role description
            with open(f'{roles_path}/{collection_name}/{role_name}/meta/main.yml') as f:
                meta = yaml.load(f, Loader=yaml.FullLoader)
                role["description"] = meta['role']['description']
                role["supports_multi"] = meta["role"].get("supports_multi", False)
                role["key"] = meta["role"].get("key", "name")

            qtask_file_names = os.listdir(f'{roles_path}/{collection_name}/{role_name}/tasks')
            for qtask_file_name in qtask_file_names:
                # continue if the file is not a yml file
                if not qtask_file_name.endswith('.yml'):
                    print(colored(f"Role {role_name} has a file that is not a yml file", 'yellow'))
                    continue

                qtask_name = qtask_file_name[:-4]

                if check_multi_regex(qtask_name, qtasks_to_skip):
                    continue
                
                qtask = {}
                qtask["name"] = qtask_name
                qtask["link"] = get_link(f"{role_name} / {qtask_name}")
                qtask["tasks"] = []

                with open(f'{roles_path}/{collection_name}/{role_name}/tasks/{qtask_file_name}') as f:
                    try:
                        qtask_data = yaml.load(f, Loader=yaml.FullLoader)
                    except yaml.YAMLError as exc:
                        print(colored(f"Error loading {qtask_file_name}", 'red'))
                        print(exc)
                        exit(1)

                    if not qtask_data:
                        print(colored(f"Error loading {qtask_file_name}", 'red'))
                        continue

                    # check if the qtask_data is a list and has length > 0
                    if not isinstance(qtask_data, list) or len(qtask_data) == 0:
                        print(colored(f"Role {role_name} qtask {qtask_name} is not a list or is empty", 'yellow'))
                        continue

                    if 'name' not in qtask_data[0]:
                        print(colored(f"Role {role_name} qtask {qtask_name} does not have a name property", 'yellow'))
                    else:
                        print(colored(f"Role {role_name} qtask {qtask_data[0]['name']}", 'magenta'))

                        # name of qtask must be "Role - {collection_name}/{role}/{qtask}"
                        if qtask_data[0]['name'] != f"Role - {collection_name}/{role_name}/{qtask_name}":
                            print(colored(f"Role {role_name} qtask {qtask_name} name is not correct", 'yellow'))
                            print(colored(f"Role {role_name} qtask {qtask_name} name should be 'Role - {collection_name}/{role_name}/{qtask['name']}'", 'yellow'))
                            print(colored(f"Role {role_name} qtask {qtask_name} name is '{qtask_data[0]['name']}'", 'yellow'))

                    # every qtask_data should have block property that is list
                    if 'block' not in qtask_data[0]:
                        print(colored(f"Role {role_name} qtask {qtask_name} does not have a block property", 'yellow'))                            
                        continue

                    tasks = qtask_data[0]['block']

                    # tasks must be a list
                    if not isinstance(tasks, list):
                        print(colored(f"Role {role_name} qtask {qtask} block is not a list", 'yellow'))
                        continue

                    for task in tasks:

                        if 'name' not in task:
                            print(colored(f"Role {role_name} qtask {qtask} has a task without a name", 'grey'))
                            continue

                        task['name'] = drop_multi_regex(task['name'], task_parts_to_drop)
                        task['link'] = task['name'].lower().replace(' ', '-')

                        if check_multi_regex(task['name'], tasks_to_skip):
                            continue

                        qtask["tasks"].append(task)

                role["qtasks"].append(qtask)
            
            template_to_file(
                'role_readme.md.j2',
                f'{roles_path}/{collection_name}/{role_name}/README.md',
                {"collection_name": collection_name, "role": role},
            )
            collection["roles"].append(role)

        template_to_file(
            'collection_readme.md.j2',
            f'{roles_path}/{collection_name}/README.md',
            {"collection": collection},
        )
        collections.append(collection)

    template_to_file(
        'collections_readme.md.j2',
        f'{roles_path}/README.md',
        {"collections": collections},
    )
    



document_roles() 