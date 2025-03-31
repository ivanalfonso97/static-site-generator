from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    # markdown = markdown.strip()

    # lines = markdown.splitlines()
    # cleaned_lines = [line.lstrip() for line in lines]
    # cleaned_markdown = "\n".join(cleaned_lines)

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
