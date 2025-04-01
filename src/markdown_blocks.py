from enum import Enum
from htmlnode import LeafNode, ParentNode
from inline_markdown import (
    text_to_textnodes,
    convert_textnodes_to_htmlnodes
)
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    return [block.strip() for block in blocks if block.strip() != ""]

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    for i, line in enumerate(lines, start=1):
        if not line.startswith(f"{i}. "):
            break
        else:
            return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    child_nodes = []
    for markdown_block in markdown_blocks:
        type = block_to_block_type(markdown_block)
        child_nodes.append(block_to_html(markdown_block, type))
    return ParentNode("div", child_nodes)

def block_to_html(block, type):
    match (type):
        case BlockType.HEADING:
            return block_to_heading(block)
        case BlockType.CODE:
            return block_to_code(block)
        case BlockType.QUOTE:
            return block_to_blockquote(block)
        case BlockType.UNORDERED_LIST:
            return block_to_unordered_list(block)
        case BlockType.ORDERED_LIST:
            return block_to_ordered_list(block)
        case _:
            return block_to_paragraph(block)

def block_to_heading(block):
    heading_md, text = block.split(" ", 1)
    html_nodes = convert_textnodes_to_htmlnodes(text_to_textnodes(text))
    return ParentNode(f"h{len(heading_md)}", html_nodes)

def block_to_code(block):
    lines = block.strip().split("\n")
    code_lines = lines[1:-1]
    code_text = "\n".join(code_lines)
    return ParentNode("pre", [LeafNode("code", code_text)])

def block_to_blockquote(block):
    lines = block.strip().split("\n")
    quote_text = " ".join([re.sub(r"^>\s?", "", line) for line in lines])
    html_nodes = convert_textnodes_to_htmlnodes(text_to_textnodes(quote_text))
    return ParentNode("blockquote", html_nodes)

def block_to_unordered_list(block):
    lines = block.strip().split("\n")
    new_list = [line.removeprefix("- ").strip() for line in lines]

    list_nodes = []
    for list_item in new_list:
        html_nodes = convert_textnodes_to_htmlnodes(text_to_textnodes(list_item))
        list_nodes.append(ParentNode("li", html_nodes))
    return ParentNode("ul", list_nodes)

def block_to_ordered_list(block):
    lines = block.strip().split("\n")
    new_list = [re.sub(r"^\d+\.\s+", "", line).strip() for line in lines]

    list_nodes = []
    for list_item in new_list:
        html_nodes = convert_textnodes_to_htmlnodes(text_to_textnodes(list_item))
        list_nodes.append(ParentNode("li", html_nodes))
    return ParentNode("ol", list_nodes)

def block_to_paragraph(block):
    normalized = block.replace("\n", " ")
    html_nodes = convert_textnodes_to_htmlnodes(text_to_textnodes(normalized))
    return ParentNode("p", html_nodes)

def extract_title(markdown):
    markdown_blocks = markdown_to_blocks(markdown)

    for block in markdown_blocks:
        if block.startswith("# "):
            return block.lstrip("# ").strip()

    raise Exception("Title not found")
