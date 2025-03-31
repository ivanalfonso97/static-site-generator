import os
import shutil
from markdown_blocks import extract_title, markdown_to_html_node

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

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    if not os.path.exists(from_path):
        raise Exception("Source path does not exist", from_path)
    if not os.path.exists(template_path):
        raise Exception("Template path does not exist", template_path)
    if not os.path.exists(dest_path):
        raise Exception("Destination path does not exist", dest_path)

    with open(from_path, "r", encoding="utf-8") as f:
        markdown = f.read()
        content = markdown_to_html_node(markdown).to_html()
        title = extract_title(markdown)

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    html = template.replace("{{ Title }}", title).replace("{{ Content }}", content)

    index_html_path = os.path.join(dest_path, "index.html")
    with open(index_html_path, "w", encoding="utf-8") as f:
        f.write(html)
