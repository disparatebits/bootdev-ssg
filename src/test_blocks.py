import unittest

from blocks import markdown_to_blocks, block_to_block_type, markdown_to_html_node, get_heading_level


class TestMarkdownToBlocks(unittest.TestCase):
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

    def test_markdown_to_blocks_empty(self):
        blocks = markdown_to_blocks("")
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_whitespace(self):
        blocks = markdown_to_blocks("  \n \n \n        ")
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_codeblock_emoji(self):
        md = """
```python3 script.py```
\n
\n
\n
               
🎉
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ['```python3 script.py```', '🎉'])

    def test_block_to_block_type(self):
        md = """
# This is a heading!
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
    """
        block = markdown_to_blocks(md)
        block_to_block_type(block[0])

    def test_block_get_heading_level(self):
        md = """
# This is a h1 heading!

## This is a h2 heading!

### This is a h3 heading!

#### This is a h4 heading!

##### This is a h5 heading!

###### This is a h6 heading!

"""
        blocks = markdown_to_blocks(md)
        for i, block in enumerate(blocks):
            level = get_heading_level(block)
            self.assertEqual(level, i + 1)

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

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )