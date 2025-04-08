#! /usr/bin/env python 
# Run this script to create a new role in the roles folder
# The script will prompt for the role collection, role name, role friendly name, allow multiple actions and actions


import os
import shutil
import sys
import jinja2

templates_path = "../templates"
roles_path = "../roles"

# set the path to the script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def log(t):
    print(t)

def make_dir(path):
    log(f"Creating directory {path}")
    os.makedirs(path, exist_ok=True)

def copy_dir(src, dest):
    log(f"Copying {src} to {dest}")
    try:
        shutil.copytree(src, dest)
    except FileExistsError:
        log(f"Directory {dest} already exists")
        pass


def template_to_file(template, file, vars, check=False):
    if check and os.path.exists(file):
        return
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(templates_path))
    template = env.get_template(template)
    output = template.render(vars)
    output = output.replace("{|{","{{")
    output = output.replace("}|}","}}")
    log(f"Deploying template {template} to {file}")
    with open(file, 'w') as f:
        f.write(output)        

def create_role(collection_name,role_name, role_description, role_key, supports_multi, actions):

    log(f"Creating role {role_name} in collection {collection_name}")

    # check if multiple actions are allowed
    supports_multi = supports_multi == "yes"

    # create the role folder
    role_path = f"{roles_path}/{collection_name}/{role_name}"
    make_dir(role_path)

    # copy the meta folder
    meta_path = f"{role_path}/meta"
    make_dir(meta_path)
    # create the meta main.yml file
    template_to_file(
        'role_template/meta/main.yml.j2',
        f'{meta_path}/main.yml',
        {},
    )
    # create the meta meta.yml file
    template_to_file(
        'role_template/meta/meta.yml.j2',
        f'{meta_path}/meta.yml',
        {"role_name": role_name, "role_description": role_description, "role_key": role_key, "supports_multi": supports_multi},
    )    

    # create the tasks folder
    log("Creating tasks folder")
    tasks_path = f"{role_path}/tasks"
    os.makedirs(tasks_path, exist_ok=True)

    # copy the facts.yml file
    template_to_file(
        'role_template/tasks/facts.yml.j2',
        f'{tasks_path}/facts.yml',
        {"role_name": role_name},
    )

    # copy the main.yml file
    template_to_file(
        'role_template/tasks/main.yml.j2',
        f'{tasks_path}/main.yml',
        {"role_name": role_name},
    )

    if supports_multi:
        # copy the facts_multi.yml file
        template_to_file(
            'role_template/tasks/facts_multi.yml.j2',
            f'{tasks_path}/facts_multi.yml',
            {"role_name": role_name},
        )

        # copy the action_multi.yml and action_one file for each action
        for action in actions:
            template_to_file(
                'role_template/tasks/action_multi.yml.j2',
                f'{tasks_path}/{action}_multi.yml',
                {"role_name": role_name, "action": action},
            )
            template_to_file(
                'role_template/tasks/action_one.yml.j2',
                f'{tasks_path}/{action}_one.yml',
                {"role_name": role_name, "action": action},
            )

    # copy the action.yml file
    for action in actions:
        template_to_file(
            'role_template/tasks/action.yml.j2',
            f'{tasks_path}/{action}.yml',
            {"collection_name":collection_name,"role_name": role_name, "action": action},
        )


# def to prompt for input, with default values and limited list values

def prompt_input(prompt, default=None, allowed_values=None, help_text=None):
    if default:
        prompt = f"{prompt} [{default}]: "
    else:
        prompt = f"{prompt}: "

    while True:
        print("---------------------------")
        if help_text:
            print(f"Help : {help_text}")        
        value = input(prompt)
        if not value:
            value = default

        if allowed_values and value not in allowed_values:
            print(f"Invalid value. Allowed values are: {allowed_values}")
            continue

        return value


if __name__ == "__main__":

    collection_name = prompt_input("Enter role collection","ontap", help_text="The role collection, like ontap, vmware, ...")
    role_name = prompt_input("Enter role name", help_text="The name of the role, like volume, svm, qtree, ...")
    role_description = prompt_input("Enter role friendly name", help_text="The friendly name of the role, like 'Create ontap volume', 'Create ontap svm', ...")
    role_key = prompt_input("Enter role key", "name", help_text="The key used to identify the role, like 'name' ...")
    supports_multi = prompt_input("Allow multiple", "no", ["yes", "no"], help_text="Allow multiple (list based) actions?")
    actions = prompt_input("Enter actions (comma separated)", help_text="The actions of the role, like 'create', 'delete', 'modify', ...").split(",")

    log(f"Role collection: {collection_name}")
    log(f"Role name: {role_name}")
    log(f"Role friendly name: {role_description}")
    log(f"Allow multiple: {supports_multi}")
    log(f"Actions: {actions}")

    create_role(collection_name, role_name, role_description, role_key, supports_multi, actions)
