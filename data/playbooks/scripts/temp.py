import os
import yaml
import sys
from termcolor import colored

# set current working directory to the directory of this script
os.chdir(os.path.dirname(os.path.realpath(__file__)))

collections = os.listdir('../roles')
for collection in collections:

    if not os.path.isdir(f'../roles/{collection}'):
        continue

    print(colored(f'Processing collection {collection}', 'green'))

    roles = os.listdir(f'../roles/{collection}')
    for role in roles:

        if not os.path.isdir(f'../roles/{collection}/{role}'):
            continue

        if os.path.exists(f'../roles/{collection}/{role}/meta/main.yml'):
            # read the meta/main.yml file
            print(f'Processing role {role}')

            # if os.path.exists(f'../roles/{collection}/{role}/meta/meta.yml'):
            #     continue

            with open(f'../roles/{collection}/{role}/meta/main.yml', 'r') as f:
                meta_main = yaml.safe_load(f)
                # meta_meta = {}
                # extract the role key and values
                # role_info = meta_main.get('role', {})
                # meta_meta['role'] = role_info

                # # write the role key and values to the meta/meta.yml file
                # with open(f'../roles/{collection}/{role}/meta/meta.yml', 'w') as f:
                #     yaml.dump(meta_meta, f)

            # remove the role key and values from the meta/main.yml file
            with open(f'../roles/{collection}/{role}/meta/main.yml', 'w') as f:
                # remove the role key and values from the meta/main.yml file
                if 'role' in meta_main:
                    del meta_main['role']
                yaml.dump(meta_main, f)
