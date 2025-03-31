from textnode import TextNode, TextType
from utils import copy_images_to_public
import os

def main():
    current_directory = os.path.abspath(__file__)
    base_directory = os.path.dirname(os.path.dirname(current_directory))
    public_directory = os.path.join(base_directory, "public")
    static_directory = os.path.join(base_directory, "static")

    copy_images_to_public(static_directory, public_directory)

main()
