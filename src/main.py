from utils import copy_images_to_public, generate_pages_recursive
import os

def main():
    current_directory = os.path.abspath(__file__)
    base_directory = os.path.dirname(os.path.dirname(current_directory))
    public_directory = os.path.join(base_directory, "public")
    static_directory = os.path.join(base_directory, "static")

    markdown_path = os.path.join(base_directory, "content")
    template_path = os.path.join(base_directory, "template.html")
    destination_directory = os.path.join(base_directory, "public")

    copy_images_to_public(static_directory, public_directory)
    generate_pages_recursive(markdown_path, template_path, destination_directory)

main()
