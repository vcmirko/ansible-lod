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
qtasks_to_skip = ["main", "facts", r".*_one$", r".*_multi$", r"^facts_.*", r"^_.*"]
# below are the keys in an ansible task that should be skipped, the goal is to keep only the key of the module
# it will typically be the first key after the name key
# however, let's at least check if the key is not in the following list
task_keys_to_skip = ["name","tags","block","loop","loop_control","when","include_vars","import_tasks","import_role","import_vars","assert","fail","debug","pause","meta","include"]
task_module_keys_string = ["include_tasks"]
task_module_keys_to_skip = ["auth_rest"]
task_module_no_vars = ["debug","pause","meta","include","fail","assert","set_fact","set_facts","unknown"]
tasks_to_skip = ["Set authentication facts","Logging","Set facts"]
task_parts_to_drop = [r"\[.*\]"]
templates_path = '../templates' 
roles_path = '../roles'   
filter_plugins_path = '../filter_plugins'
modules_path = '../library'      
playbooks_path = '../'
playbooks_to_add = [r".*"]
playbooks_to_skip = [r"^inventory",r"^test"]
playbook_qtasks_to_skip = [r"^facts"]

# set the path to the script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# finds something like this: and grabs the headers with values
# # =========================================================
# # DESCRIPTION:
# # Some description
# # Some more description
# #
# # VERSION HISTORY:
# # 2025-02-03 - Mirko Van Colen - Initial version
# # =========================================================
def find_commented_lines(file,headers_to_find=["description","version history"]):

    # convert the headers to uppercase
    headers_to_find = [header.upper() for header in headers_to_find]

    # read the file
    with open(file) as f:
        lines = f.readlines()

    # find the start and end of the comment block
    start = None
    end = None
    for i, line in enumerate(lines):
        if line.startswith("# ====="):
            if start is None:
                start = i
            else:
                end = i
                break
    
    if start is None or end is None:
        return {}
    
    # extract the lines between the start and end
    lines = lines[start:end]

    # remove the comment character and the space
    lines = [line[2:].strip() for line in lines]

    # find the headers and the content
    headers = {}

    for i, line in enumerate(lines):
        if line in headers_to_find:
            header_name = line.lower().replace(" ","_")
            headers[header_name] = ""
            for j in range(i+1, len(lines)):
                if lines[j] in headers_to_find:
                    break
                headers[header_name] += lines[j] + "<br>"

    # remove all trailing <br> from the headers

    for header in headers:
        headers[header] = headers[header].strip("<br>")

    return headers

def find_file_headers(path, allowed_extensions=[".py"], includes=[".*"], excludes=[""]):
    # for each .py file, find the commented lines
    if not os.path.exists(path):
        return []

    list_of_files = []

    # print(colored(f"Processing path {path}", 'yellow'))

    file_names = os.listdir(path)
    for file_name in file_names:

        # if directory, skip
        if os.path.isdir(f"{path}/{file_name}"):
            continue

        # print(colored(f"Processing file {file_name}", 'yellow'))

        # check if the file is an allowed extension
        if not any([file_name.endswith(ext) for ext in allowed_extensions]):
            continue

        # check if the file is in the includes
        if not check_multi_regex(file_name, includes):
            continue

        # check if the file is in the excludes
        if check_multi_regex(file_name, excludes):
            continue

        # print(colored(f"Processing file for headers {file_name}", 'cyan'))

        headers = find_commented_lines(f"{path}/{file_name}")

        # print(headers)
        object = {}
        object["name"] = file_name
        object["link"] = get_link(file_name)
        for header in headers:
            object[header] = headers[header]

        object["defs"] = find_regex_group_with_comments(f"{path}/{file_name}")

        list_of_files.append(object)
    return list_of_files

def find_regex_group_with_comments(file, regex=r"^def ([^(]+)\(", comments_char="#", exclude=["filters"]):

    with open(file) as f:
        lines = f.readlines()

    results = {}
    for i, line in enumerate(lines):
        line = line.strip() 
        if re.match(regex, line):
            # find the def name
            def_name = re.match(regex, line).group(1)
            # find the comment lines above the def
            comments = []
            for j in range(i-1, -1, -1):
                if lines[j].strip().startswith(comments_char):
                    comments.append(lines[j].strip()[1:])
                else:
                    break
            comments = "<br>".join(comments)
            results[def_name] = comments

    # remove the excluded items
    for item in exclude:
        if item in results:
            del results[item]

    return results

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
    return name.lower().replace(' ', '-').replace('/','').replace('.','')

def document_roles():

    filter_plugins = find_file_headers(f'{filter_plugins_path}')
    modules = find_file_headers(f'{modules_path}')

    template_to_file(
        'library_readme.md.j2',
        f'{modules_path}/README.md',
        {"modules": modules},
    )

    template_to_file(
        'filter_plugins_readme.md.j2',
        f'{filter_plugins_path}/README.md',
        {"filters": filter_plugins},
    )

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

            # process library
            role["modules"] = find_file_headers(f'{roles_path}/{collection_name}/{role_name}/library')

            # process filters
            role["filters"] = find_file_headers(f'{roles_path}/{collection_name}/{role_name}/filter_plugins')

            # process qtasks
            role["qtasks"] = []

            if not os.path.exists(f'{roles_path}/{collection_name}/{role_name}/tasks'):
                # print with color
                print(colored(f"Role {role_name} does not have a tasks folder", 'red'))
                continue

            # check if the role has a meta folder with main.yml file
            if not os.path.exists(f'{roles_path}/{collection_name}/{role_name}/meta'):
                print(colored(f"Role {role_name} does not have a meta folder", 'yellow'))
                continue

            # get the role description
            with open(f'{roles_path}/{collection_name}/{role_name}/meta/meta.yml') as f:
                meta = yaml.load(f, Loader=yaml.FullLoader)
                role["description"]    = meta.get('role',{}).get('description', '-- Missing description --')
                role["supports_multi"] = meta.get("role",{}).get("supports_multi", False)
                role["key"]            = meta.get("role",{}).get("key", "name")

            # let's load all the qtasks
            qtask_file_names = os.listdir(f'{roles_path}/{collection_name}/{role_name}/tasks')
            for qtask_file_name in qtask_file_names:

                # continue if the file is not a yml file
                # we simple only summport yml files (not yaml files)
                if not qtask_file_name.endswith('.yml'):
                    print(colored(f"Role {role_name} has a file that is not a yml file", 'yellow'))
                    continue

                # the raw qtask name
                qtask_name = qtask_file_name[:-4]

                # check if the qtask name is in the skip list
                if check_multi_regex(qtask_name, qtasks_to_skip):
                    continue
                
                # create a qtask object
                qtask = {}
                qtask["name"] = qtask_name
                qtask["link"] = get_link(f"{role_name} / {qtask_name}")
                qtask["tasks"] = []
                qtask["vars"] = []
                qtask_vars = {}

                # read the qtask file
                with open(f'{roles_path}/{collection_name}/{role_name}/tasks/{qtask_file_name}') as f:

                    # check if valid yaml
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

                    # check if the qtask has a name property (+ block)
                    if 'name' not in qtask_data[0]:
                        print(colored(f"Role {role_name} qtask {qtask_name} does not have a name property", 'yellow'))
                    else:
                        print(colored(f"Role {role_name} qtask {qtask_data[0]['name']}", 'magenta'))

                        # name of qtask must be format "Role - {collection_name}/{role}/{qtask}"
                        if qtask_data[0]['name'] != f"Role - {collection_name}/{role_name}/{qtask_name}":
                            print(colored(f"Role {role_name} qtask {qtask_name} name is not correct", 'yellow'))
                            print(colored(f"Role {role_name} qtask {qtask_name} name should be 'Role - {collection_name}/{role_name}/{qtask['name']}'", 'yellow'))
                            print(colored(f"Role {role_name} qtask {qtask_name} name is '{qtask_data[0]['name']}'", 'yellow'))

                    # every qtask_data should have block property that is list
                    if 'block' not in qtask_data[0]:
                        print(colored(f"Role {role_name} qtask {qtask_name} does not have a block property", 'yellow'))                            
                        continue

                    # there be block property with the tasks
                    # it's part of the maf format
                    tasks = qtask_data[0]['block']

                    # tasks must be a list
                    if not isinstance(tasks, list):
                        print(colored(f"Role {role_name} qtask {qtask} block is not a list", 'yellow'))
                        continue

                    # let's loop all the tasks within the qtask role yaml file
                    for task in tasks:

                        # every task must have a name property
                        if 'name' not in task:
                            print(colored(f"Role {role_name} qtask {qtask} has a task without a name", 'grey'))
                            continue

                        # remove unwanted parts from the name (mainly dynamic parts like [svm_name])
                        # so put dynamic parts in square brackets
                        task['name'] = drop_multi_regex(task['name'], task_parts_to_drop)

                        # create a title md link for the task
                        task['link'] = task['name'].lower().replace(' ', '-')

                        # skip certain tasks
                        if check_multi_regex(task['name'], tasks_to_skip):
                            continue

                        # analyze the task
                        keys = list(task.keys())
                        task['module'] = "unknown"
                        task['collection'] = ""
                        task['vars'] = []
                        task['looped'] = False
                        vars = {}
                        loop_var = None
                        loop = None

                        # there must be at least 2 keys in the task (name + module)
                        if len(keys) > 1 :

                            # lets take the 2nd key in the task, assuming the first is the name, and the 2nd is the module name
                            module_name = keys[1]
                            # split on last dot to get the module name and collection name
                            if "." in module_name:
                                # split on last dot
                                collection_module = module_name.rsplit(".",1)
                                task['module'] = collection_module[1]
                                task['collection'] = collection_module[0]
                            else:
                                task['module'] = module_name

                            # find the input data for the module, assuming the module is a dict
                            subkeys = []

                            # check if thm module is looped
                            # add the loop as module input, because it's important for the vars
                            if "loop" in keys:
                                task["looped"] = True

                                # track the loop var (we will exclude this from the vars)
                                if "loop_control" in keys:
                                    if "loop_var" in task["loop_control"]:
                                        loop_var = task["loop_control"].get("loop_var","item")

                                # add the loop to input vars
                                subkeys.append("loop")
                                if(isinstance(task[module_name], str)):
                                    task[module_name] = {}
                                loop = task["loop"]
                                task[module_name]["loop"] = loop

                            if isinstance(task[module_name], dict):
                                subkeys = list(task[module_name].keys())

                            # analyse the input data, we will search for {{ var.property ... optional filter }}
                            for subkey in subkeys:
                                value = task[module_name][subkey]
                                # only process strings
                                if isinstance(value, str):
                                    # remove all spaces and quota's
                                    value = value.replace(" ","").replace("'","").replace('"','')
                                    # check if the value is a jinja2 template
                                    if value.startswith("{{") and value.endswith("}}"):
                                        # remove the jinja2 template characters
                                        value = value[2:-2]
                                        # remove the filter part if any
                                        if "|" in value:
                                            value = value.split("|")[0]
                                        # if no dot, continue
                                        var = value
                                        property = ""
                                        if "." in value:
                                            # grab the input variable and the property
                                            var = value.split(".")[0]
                                            property = value.split(".")[1]

                                        # skip certain vars (like auth_rest)
                                        if var not in task_module_keys_to_skip and task['module'] not in task_module_no_vars and loop_var!=var:
                                            # group the properties per var
                                            # keep track on qtask level and ond task level
                                            if var not in qtask_vars:
                                                qtask_vars[var] = {}                                            
                                                qtask_vars[var]['name'] = var
                                                qtask_vars[var]["properties"] = []
                                            if var not in vars:
                                                vars[var] = {}
                                                vars[var]['name'] = var
                                                vars[var]['properties'] = []
                                            if property not in vars[var]['properties']:
                                                vars[var]['properties'].append(property)
                                            if property not in qtask_vars[var]['properties']:
                                                qtask_vars[var]['properties'].append(property)

                            # all input data is analyzed, let's add the vars to the task, order them alphabetically
                            for var in sorted(vars):
                                task['vars'].append(vars[var])

                        qtask["tasks"].append(task)

                    # // end of task loop


                    for var in sorted(qtask_vars):
                        qtask['vars'].append(qtask_vars[var])

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
    
    # get playbooks (all yaml files, no inventory)
    playbooks = find_file_headers(playbooks_path,[".yaml",".yml"],playbooks_to_add,playbooks_to_skip)

    for playbook in playbooks:

        playbook_name = playbook["name"]

        # read the playbook from yaml
        with open(f'{playbooks_path}/{playbook_name}') as f:
            plays = yaml.load(f, Loader=yaml.FullLoader)

        # if not a list, continue
        if not isinstance(plays, list):
            continue

        # if empty, continue
        if len(plays) == 0:
            continue

        # play.roles => remove all roles with qtask containing "facts"
        for play in plays:
            if "roles" in play:
                play["roles"] = [role for role in play["roles"] if not any([check_multi_regex(role["qtask"], playbook_qtasks_to_skip)])]

        print(colored(f"Playbook {playbook_name}", 'blue'))    
        playbook["plays"] = plays


    # process template
    template_to_file(
        'playbooks_readme.md.j2',
        f'{playbooks_path}/README_playbooks.md',
        {"playbooks": playbooks},
    )



document_roles() 