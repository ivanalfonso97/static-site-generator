from textnode import TextType, TextNode
from htmlnode import LeafNode
import re

def text_node_to_html_node(text_node):
    match (text_node.text_type):
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Text type not allowed")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if (
            node.text_type != TextType.TEXT or
            delimiter not in node.text
        ):
            new_nodes.append(node)
            continue

        sections = node.text.split(delimiter)

        if len(sections) % 2 == 0:
            raise Exception("Unbalanced delimiter pairs in text")

        for i, part in enumerate(sections):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        current_text = node.text
        found_images = extract_markdown_images(node.text)

        if len(found_images) == 0:
            new_nodes.append(node)
            continue

        for alt_text, url in found_images:
            markdown = f"![{alt_text}]({url})"
            sections = current_text.split(markdown, maxsplit=1)

            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            current_text = sections[1]

        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        current_text = node.text
        found_links = extract_markdown_links(node.text)

        if len(found_links) == 0:
            new_nodes.append(node)
            continue

        for link_text, url in found_links:
            markdown = f"[{link_text}]({url})"
            sections = current_text.split(markdown, maxsplit=1)

            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(TextNode(link_text, TextType.LINK, url))
            current_text = sections[1]

        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))

    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def convert_textnodes_to_htmlnodes(text_nodes):
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes
