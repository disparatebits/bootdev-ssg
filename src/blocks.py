import re
from enum import Enum

from htmlnode import ParentNode, LeafNode
from textnode import text_node_to_html_node, text_to_textnodes


class BlockType(Enum):
    PARA = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED = 'unordered_list'
    ORDERED = 'ordered_list'


def markdown_to_blocks(markdown):
    blocks = list(markdown.split("\n\n"))
    result = []
    for block in blocks:
        block = block.strip()
        if block:
            result.append(block)
    return result


def block_to_block_type(block):
    lines = block.split("\n")

    if block[0] == '#':
        return BlockType.HEADING
    elif block[0:3] == '```' and block[-3:] == '```':
        return BlockType.CODE
    elif all(line.startswith('>') for line in lines):
        return BlockType.QUOTE
    elif all(line.startswith('-') for line in lines):
        return BlockType.UNORDERED
    elif is_ordered_list(lines):
        return BlockType.ORDERED
    else:
        return BlockType.PARA


def is_ordered_list(lines):
    if not lines:
        return False
    for idx, line in enumerate(lines):
        expected = f"{idx + 1}."
        if not line.startswith(expected):
            return False
    return True


def handle_list_items(text):
    lines = text.split("\n")
    li_nodes = []


    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line[0] in {'-', '+', '*'}:
            content = line[1:].strip()
        elif line[0].isdigit() and line[1] == '.':
            content = line[2:].strip()
        else:
            continue

        if content.strip():
            children = text_to_children(content)
            li_node = ParentNode(tag='li', children=children)
            li_nodes.append(li_node)

    return li_nodes


def text_to_children(block):
    text_nodes = text_to_textnodes(block)
    html_nodes = []
    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        html_nodes.append(html_node)

    return html_nodes


def get_heading_level(block):
    if not block.startswith('#'):
        return 0
    count = 0
    for char in block:
        if char == '#':
            count += 1
        else:
            break

    if count < len(block) and block[count] == ' ':
        return count
    else:
        return 0


def has_inline_formatting(content):
    inline_pattern = r"(\*\*.*?\*\*?\*\*|_.*?_|`.*?`)"
    return re.search(inline_pattern, content) is not None


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    parent = ParentNode(tag='div', children=[])
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARA:
                # Normalize whitespace in paragraph text
                import re
                normalized_block = re.sub(r'\s+', ' ', block).strip()
                p_node = ParentNode(tag='p', children=text_to_children(normalized_block))
                parent.children.append(p_node)
            case BlockType.HEADING:
                level = get_heading_level(block)
                content = block[level + 1:].strip()
                if has_inline_formatting(content):
                    h_node = ParentNode(tag=f"h{level}", children=text_to_children(content))
                else:
                    h_node = LeafNode(tag=f"h{level}", value=content)
                parent.children.append(h_node)
            case BlockType.UNORDERED:
                ul_node = ParentNode(tag='ul', children=handle_list_items(block))
                parent.children.append(ul_node)
            case BlockType.ORDERED:
                ol_node = ParentNode(tag='ol', children=handle_list_items(block))
                parent.children.append(ol_node)
            case BlockType.QUOTE:
                quote_node = ParentNode(tag='blockquote', children=text_to_children(block))
                parent.children.append(quote_node)
            case BlockType.CODE:
                content = '\n'.join(block.split('\n')[1:-1])
                content += '\n'
                code_node = LeafNode(tag='code', value=content)
                pre_node = ParentNode(tag='pre', children=[code_node])
                parent.children.append(pre_node)

    return parent
