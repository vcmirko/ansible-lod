#!/bin/bash

# Define temporary directory
tmp_dir="/tmp"

# Clone the repository
git clone https://github.com/vcmirko/ansible-lod.git "$tmp_dir/ansible-lod"

# Check if the clone was successful
if [ $? -eq 0 ]; then
    echo "Repository cloned successfully."

    # Define source and target directories
    src_base_dir="$tmp_dir/ansible-lod/data"
    target_dir="/srv/apps/ansible-lod/data"

    # Define an array of directories and files to process
    items=("playbooks" "forms" "forms.yaml")

    for item in "${items[@]}"; do
        src_item="$src_base_dir/$item"
        
        # Check if the source item exists
        if [ -e "$src_item" ]; then
            if [ -d "$src_item" ]; then
                # Remove the target directory if it already exists
                if [ -d "$target_dir/$item" ]; then
                    echo "Removing existing target directory: $target_dir/$item"
                    rm -rf "$target_dir/$item"
                fi

                # Move the source directory to the target location
                mv "$src_item" "$target_dir"
                echo "Moved $src_item to $target_dir"
            else
                # Copy the source file to the target location
                cp -i "$src_item" "$target_dir"
                echo "Copied $src_item to $target_dir"
            fi
        else
            echo "Source item $src_item not found."
        fi
    done
else
    echo "Failed to clone the repository."
fi

# Clean up the temporary directory
rm -rf "$tmp_dir/ansible-lod"

echo "Temporary directory cleaned up."