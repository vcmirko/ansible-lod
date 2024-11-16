#! /usr/bin/env python 
# Run this script to create a new role in the roles folder
# The script will prompt for the role collection, role name, role friendly name, allow multiple actions and actions


import os
import shutil
import sys

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

def copy_file(src, dest):
    log(f"Copying {src} to {dest}")
    try:
        shutil.copyfile(src, dest)
    except FileExistsError:
        log(f"File {dest} already exists")
        pass

def create_role(role_collection,role_name, role_friendly_name, allow_multiple, actions):

    log(f"Creating role {role_name} in collection {role_collection}")

    # check if multiple actions are allowed
    allow_multiple = allow_multiple == "yes"

    # create the role folder
    role_path = f"{role_collection}/{role_name}"
    make_dir(role_path)

    # copy the meta folder
    meta_path = f"{role_path}/meta"
    copy_dir("role_template/meta", meta_path)

    # create the tasks folder
    log("Creating tasks folder")
    tasks_path = f"{role_path}/tasks"
    os.makedirs(tasks_path, exist_ok=True)

    # copy the main.yml file
    copy_file("./role_template/tasks/main.yml", f"./{tasks_path}/main.yml")

    # copy the facts.yml file
    copy_file("role_template/tasks/facts.yml", f"{tasks_path}/facts.yml")

    # copy the action.yml file
    for action in actions:
        copy_file("role_template/tasks/action.yml", f"{tasks_path}/{action}.yml")
        replace_variables_in_file(f"{tasks_path}/{action}.yml", role_collection, role_name, action)

    if allow_multiple:
        # copy the action_one.yml file
        for action in actions:
            copy_file("role_template/tasks/action_one.yml", f"{tasks_path}/{action}_one.yml")
            copy_file("role_template/tasks/action_multi.yml", f"{tasks_path}/{action}_multi.yml")
            replace_variables_in_file(f"{tasks_path}/{action}_one.yml", role_collection, role_name, action)
            replace_variables_in_file(f"{tasks_path}/{action}_multi.yml", role_collection, role_name, action)

        copy_file("role_template/tasks/facts_multi.yml", f"{tasks_path}/facts_multi.yml")

    # copy the README.MD file
    copy_file("role_template/README.md", f"{role_path}/README.md")

    # replace the variables in the files
    replace_variables_in_folder(role_path, role_collection, role_name, role_friendly_name)

def replace_variables_in_file(file_path, role_collection, role_name, action):
    with open(file_path, "r") as f:
        content = f.read()
    content = content.replace("<action>", action)
    content = content.replace("<role_name>", role_name)
    content = content.replace("<role_collection>", role_collection)
    with open(file_path, "w") as f:
        f.write(content)

def replace_variables_in_folder(role_path, role_collection, role_name, role_friendly_name):
    # replace the variables in all files in the role folder
    log("Replacing variables in files")
    for root, _, files in os.walk(role_path):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, "r") as f:
                content = f.read()
            content = content.replace("<role_name>", role_name)
            content = content.replace("<role_friendly_name>", role_friendly_name)
            content = content.replace("<role_collection>", role_collection)

            with open(file_path, "w") as f:
                f.write(content)

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

    role_collection = prompt_input("Enter role collection","ontap", help_text="The role collection, like ontap, vmware, ...")
    role_name = prompt_input("Enter role name", help_text="The name of the role, like volume, svm, qtree, ...")
    role_friendly_name = prompt_input("Enter role friendly name", help_text="The friendly name of the role, like 'Create ontap volume', 'Create ontap svm', ...")
    allow_multiple = prompt_input("Allow multiple", "no", ["yes", "no"], help_text="Allow multiple (list based) actions?")
    actions = prompt_input("Enter actions (comma separated)", help_text="The actions of the role, like 'create', 'delete', 'modify', ...").split(",")

    log(f"Role collection: {role_collection}")
    log(f"Role name: {role_name}")
    log(f"Role friendly name: {role_friendly_name}")
    log(f"Allow multiple: {allow_multiple}")
    log(f"Actions: {actions}")

    create_role(role_collection, role_name, role_friendly_name, allow_multiple, actions)
