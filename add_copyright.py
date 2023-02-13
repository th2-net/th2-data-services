import os
import shutil

def add_text_to_file(file_path, text_path):
    # Check if file is a python script
    if not file_path.endswith('.py'):
        return

    # Read the text to be added from the argument file
    with open(text_path, 'r') as text_file:
        text = text_file.read()

    # Read the contents of the target file and throw away header comments and empty lines
    with open(file_path, 'r') as target_file:
        target = target_file.readlines()
        c = 0
        for i in target:
            if i.strip() == '' or i.strip()[0] == '#':
                c+=1
            else:
                break
        target = "".join(target[c:])

    # Add copyright text to target file's head
    with open(file_path, 'w') as target_file:
        target_file.write(text + '\n' + target)
    print("Updating " + file_path)

def add_text_to_files_in_dir(dir_path, text_path):
    # Loop through all items in the directory
    for item in os.listdir(dir_path):
        item_path = os.path.join(dir_path, item)
        # If the item is a directory, call the function recursively
        if os.path.isdir(item_path):
            add_text_to_files_in_dir(item_path, text_path)
        else:
            add_text_to_file(item_path, text_path)

if __name__ == '__main__':
    import sys
    text_path = sys.argv[1]
    dir_path = sys.argv[2]
    add_text_to_files_in_dir(dir_path, text_path)
