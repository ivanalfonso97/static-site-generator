import unittest
from markdown_blocks import (
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node,
    extract_title,
    BlockType
)
from pdb import Restart

class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_heading(self):
        md = """
## Heading 2 **Title**

Here is the rest
of my paragraph
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>Heading 2 <b>Title</b></h2><p>Here is the rest of my paragraph</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        expected = """<div><pre><code>This is text that _should_ remain
the **same** even with inline stuff</code></pre></div>""".strip()

        self.assertEqual(
            html,
            expected
        )

    def test_blockquote(self):
        md = """> This is a quote
> that spans multiple lines"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        expected = (
            "<div><blockquote><p>This is a quote that spans multiple lines</p></blockquote></div>"
        )

        self.assertEqual(html, expected)

    def test_unordered_list(self):
        md = """- Item one
- Item two
- Item three"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        expected = "<div><ul><li>Item one</li><li>Item two</li><li>Item three</li></ul></div>"
        self.assertEqual(html, expected)

    def test_ordered_list(self):
        md = """1. First item
2. Second item
3. Third item"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        expected = "<div><ol><li>First item</li><li>Second item</li><li>Third item</li></ol></div>"
        self.assertEqual(html, expected)

    def test_combined(self):
        md = """## Welcome to My Page

This is an _awesome_ paragraph with **bold text** and `inline code`.

- First bullet
- Second **bold** bullet
- Third with `code`

```
Block code
with multiple lines
```

> This is a quote
> that spans lines"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        expected = (
            "<div>"
            "<h2>Welcome to My Page</h2>"
            "<p>This is an <i>awesome</i> paragraph with <b>bold text</b> and <code>inline code</code>.</p>"
            "<ul><li>First bullet</li><li>Second <b>bold</b> bullet</li><li>Third with <code>code</code></li></ul>"
            "<pre><code>Block code\nwith multiple lines</code></pre>"
            "<blockquote><p>This is a quote that spans lines</p></blockquote>"
            "</div>"
        )

        self.assertEqual(html, expected)

    def test_extract_title(self):
        md = """# Welcome to My Page

This is an _awesome_ paragraph with **bold text** and `inline code`."""

        title = extract_title(md)
        expected = ("Welcome to My Page")

        self.assertEqual(title, expected)

    def test_extract_title_exception(self):
        md = """## Welcome to My Page

This is an _awesome_ paragraph with **bold text** and `inline code`."""

        with self.assertRaises(Exception) as context:
            extract_title(md)
            self.assertEqual(str(context.exception), "Title not found")

if __name__ == "__main__":
    unittest.main()
