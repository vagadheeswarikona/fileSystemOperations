# C:\Users\konau\OneDrive\Desktop\fileSystem\fileSystemOperation.py

import json
import os

class File:
    def __init__(self, name, content=""):
        self.name = name
        self.content = content

class Directory:
    def __init__(self, name):
        self.name = name
        self.files = []
        self.subdirectories = []

class FileSystem:
    def __init__(self):
        self.root = Directory("/")
        self.current_directory = self.root

def save_state(file_system, path):
    state = {"current_directory": file_system.current_directory.name}
    with open(path, "w") as file:
        json.dump(state, file)

def load_state(file_system, path):
    with open(path, "r") as file:
        state = json.load(file)
        file_system.current_directory = find_directory(file_system.root, state["current_directory"])

def find_directory(directory, name):
    if directory.name == name:
        return directory
    for subdir in directory.subdirectories:
        result = find_directory(subdir, name)
        if result:
            return result
    return None

def mkdir(file_system, directory_name):
    new_directory = Directory(directory_name)
    file_system.current_directory.subdirectories.append(new_directory)

def cd(file_system, path):
    if path == "/":
        file_system.current_directory = file_system.root
    else:
        file_system.current_directory = find_directory(file_system.root, path)

def ls(file_system):
    for file in file_system.current_directory.files:
        print(f"File: {file.name}")
    for subdir in file_system.current_directory.subdirectories:
        print(f"Directory: {subdir.name}")

def touch(file_system, file_name):
    new_file = File(file_name)
    file_system.current_directory.files.append(new_file)

def echo(file_system, file_name, content):
    target_file = None
    for file in file_system.current_directory.files:
        if file.name == file_name:
            target_file = file
            break
    if target_file:
        target_file.content = content
    else:
        new_file = File(file_name, content)
        file_system.current_directory.files.append(new_file)

def mv(file_system, source_path, destination_path):
    source_dir_path, source_name = os.path.split(source_path)
    dest_dir_path, dest_name = os.path.split(destination_path)

    source_directory = find_directory(file_system.root, source_dir_path)
    destination_directory = find_directory(file_system.root, dest_dir_path)

    target = None
    for item in source_directory.files + source_directory.subdirectories:
        if item.name == source_name:
            target = item
            break

    if not target:
        print(f"Error: {source_path} not found.")
        return

    source_directory.files = [item for item in source_directory.files if item != target]
    source_directory.subdirectories = [item for item in source_directory.subdirectories if item != target]

    if isinstance(target, Directory):
        target.name = dest_name

    destination_directory.subdirectories.append(target)

    print(f"Moved {source_path} to {destination_path}")

def cp(file_system, source_path, destination_path):
    source_dir_path, source_name = os.path.split(source_path)
    dest_dir_path, dest_name = os.path.split(destination_path)

    source_directory = find_directory(file_system.root, source_dir_path)
    destination_directory = find_directory(file_system.root, dest_dir_path)

    source_item = None
    for item in source_directory.files + source_directory.subdirectories:
        if item.name == source_name:
            source_item = item
            break

    if not source_item:
        print(f"Error: {source_path} not found.")
        return

    if isinstance(source_item, File):
        new_copy = File(name=dest_name, content=source_item.content)
    elif isinstance(source_item, Directory):
        new_copy = Directory(name=dest_name)

        for file in source_item.files:
            new_copy.files.append(File(name=file.name, content=file.content))
        for subdir in source_item.subdirectories:
            new_copy.subdirectories.append(cp(file_system, f"{source_path}/{subdir.name}", f"{destination_path}/{subdir.name}"))

    destination_directory.subdirectories.append(new_copy)

    print(f"Copied {source_path} to {destination_path}")

def rm(file_system, target_path):
    target_dir_path, target_name = os.path.split(target_path)

    target_directory = find_directory(file_system.root, target_dir_path)

    target_item = None
    for item in target_directory.files + target_directory.subdirectories:
        if item.name == target_name:
            target_item = item
            break

    if not target_item:
        print(f"Error: {target_path} not found.")
        return

    target_directory.files = [item for item in target_directory.files if item != target_item]
    target_directory.subdirectories = [item for item in target_directory.subdirectories if item != target_item]

    print(f"Removed {target_path}")

def main():
    file_system = FileSystem()

    # Example: Create a sample file system
    mkdir(file_system, "documents")
    cd(file_system, "documents")
    mkdir(file_system, "work")
    mkdir(file_system, "personal")
    touch(file_system, "resume.txt")
    touch(file_system, "todo.txt")

    while True:
        command = input("Enter a command: ")
        parts = command.split(" ")

        if parts[0] == "mkdir":
            mkdir(file_system, parts[1])

        elif parts[0] == "cd":
            cd(file_system, parts[1])

        elif parts[0] == "ls":
            ls(file_system)

        elif parts[0] == "touch":
            touch(file_system, parts[1])

        elif parts[0] == "echo":
            echo(file_system, parts[1], " ".join(parts[2:]))

        elif parts[0] == "mv":
            mv(file_system, parts[1], parts[2])

        elif parts[0] == "cp":
            cp(file_system, parts[1], parts[2])

        elif parts[0] == "rm":
            rm(file_system, parts[1])

        elif parts[0] == "save":
            save_state(file_system, parts[1])

        elif parts[0] == "load":
            load_state(file_system, parts[1])


if __name__ == "__main__":
    main()
