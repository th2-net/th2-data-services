import os
import re
from datetime import date
import sys

__version__ = "1.0.0"


def check_copyright(file_path, text_path):
    # Check if file is a python script
    if not file_path.endswith(".py") or "pycache" in file_path:
        return "correct"

    # Read the text to check against
    with open(text_path, "r") as text_file:
        text = text_file.readlines()
        text_header = text[0]
        text_body = text[1:]

    # Read the contents of the target file
    # Checks if target file starts with text_file ignoring leading new lines
    with open(file_path, "r", encoding="utf-8") as target_file:
        target = target_file.readlines()
        c = 0
        year = str(date.today().year)
        for i, x in enumerate(target):
            if x == "\n":
                continue
            elif x[0] == "#":
                if re.search(pattern="Copyright\s\d\d\d\d\-\d\d\d\d", string=target[i]):
                    if x[x.index("t") + 7 : x.index("t") + 11] != year:
                        return x[x.index("t") + 2 : x.index("t") + 11]
                    elif not "".join(target[i + 1 :]).startswith("".join(text_body)):
                        return x[x.index("t") + 2 : x.index("t") + 11]
                    else:
                        return "correct"
                elif re.search("Copyright \d\d\d\d", target[i]):
                    if x[x.index("t") + 2 : x.index("t") + 6] != year:
                        return x[x.index("t") + 2 : x.index("t") + 6]
                    elif not "".join(target[i + 1 :]).startswith("".join(text_body)):
                        return x[x.index("t") + 2 : x.index("t") + 6]
                    else:
                        return "correct"
                else:
                    return "correct"
            else:
                return "missing"
        return "missing"


def add_text_to_file(file_path_list, text_path):
    file_path = file_path_list[0]
    year = str(date.today().year)
    # Check if file is a python script
    if not file_path.endswith(".py") or "pycache" in file_path:
        return

    # Read the text to be added from the argument file
    with open(text_path, "r") as text_file:
        text = text_file.read()
        if len(file_path_list[1]) > 4:
            if file_path_list[1][-4:] == year:
                text = text.format(file_path_list[1])
            elif file_path_list[1] == "missing":
                text = text.format(year)
            else:
                text = text.format(file_path_list[1][:-4] + year)
        else:
            if file_path_list[1][-4:] != year:
                text = text.format(file_path_list[1] + "-" + year)
            else:
                text = text.format(year)

    # Read the contents of the target file and throw away header comments and empty lines
    with open(file_path, "r") as target_file:
        target = target_file.readlines()
        c = 0
        for i in target:
            if i == "\n":
                c += 1
            elif i[0] == "#":
                c += 13
                break
            else:
                break
        target = "".join(target[c:])

    # Add copyright text to target file's head
    with open(file_path, "w") as target_file:
        target_file.write(text + "\n" + target)
    print("Updating " + file_path)


def check_files_in_dir(dir_path, text_path, uncopyrighted_files):
    # Loop through all items in the directory
    for item in os.listdir(dir_path):
        item_path = os.path.join(dir_path, item)
        # If the item is a directory, call the function recursively
        if os.path.isdir(item_path):
            check_files_in_dir(item_path, text_path, uncopyrighted_files)
        else:
            val = check_copyright(item_path, text_path)
            if val != "correct":
                uncopyrighted_files.append([item_path, val])


if __name__ == "__main__":
    text_path = sys.argv[1]
    dir_path = sys.argv[2]
    update = False
    if len(sys.argv) == 4 and sys.argv[3] == "--update":
        update = True
    uncopyrighted_files = []
    check_files_in_dir(dir_path, text_path, uncopyrighted_files)
    if len(uncopyrighted_files):
        if update:
            for i in uncopyrighted_files:
                add_text_to_file(i, text_path)
        else:
            print("Copyright text is incorrectly placed in following files:")
            for i in uncopyrighted_files:
                print(i)
            print(
                "You can either manually fix copyright text in these files or use command like this: python3 check_copyright copyright.txt dir_location --update"
            )
            print(
                "Beware that using --update argument will remove any comment at the start of problematic files"
            )
            sys.exit(1)
    else:
        print("No problems with copyright were detected")
