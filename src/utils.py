import os
import shutil

def copy_images_to_public(source, destination):
    if not os.path.exists(source):
        raise Exception("Source path does not exist", source)
    if not os.path.exists(destination):
        raise Exception("Destination path does not exist", destination)

    shutil.rmtree(destination)
    os.mkdir(destination)

    copy_files(source, destination)

def copy_files(source, destination):
    branches = os.listdir(source)
    if len(branches) == 0:
        return

    for branch in branches:
        branch_path = os.path.join(source, branch)
        target_path = os.path.join(destination, branch)

        if os.path.isfile(branch_path):
            shutil.copy(branch_path, target_path)
        elif os.path.isdir(branch_path):
            os.mkdir(target_path)
            copy_files(branch_path, target_path)
        else:
            raise Exception("Could not identify file or directory")
