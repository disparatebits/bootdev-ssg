import re
from enum import Enum

from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode(text={self.text}, text_type={self.text_type.value}, url={self.url})"


def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches


def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(tag=None, value=text_node.text)
    match text_node.text_type:
        case TextType.BOLD:
            return LeafNode(tag='b', value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag='i', value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag='code', value=text_node.text)
        case TextType.LINK:
            return LeafNode(tag='a', value=text_node.text, props={'href': text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag='img', value='', props={'src': text_node.url,
                                                        'alt': text_node.text
                                                        })
        case _:
            raise Exception(f"Unknown TextType: {text_node.text_type}")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            parts = old_node.text.split(delimiter)
            if len(parts) == 1:
                new_nodes.append(old_node)
            elif len(parts) % 2 == 0:
                raise Exception(f"Missing delimiter: {delimiter}")
            else:
                for idx, val in enumerate(parts):
                    if idx % 2 == 0:
                        if val != "":
                            new_nodes.append(TextNode(val, text_type=TextType.TEXT))
                    else:
                        new_nodes.append(TextNode(val, text_type=text_type))
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        images = extract_markdown_images(old_node.text)
        if not images:
            new_nodes.append(old_node)
            continue

        current_text = old_node.text
        for image in images:
            parts = current_text.split(f"![{image[0]}]({image[1]})", 1)
            new_nodes.append(TextNode(parts[0], text_type=TextType.TEXT))
            new_nodes.append(TextNode(image[0], text_type=TextType.IMAGE, url=image[1]))
            current_text = parts[1]
        if current_text:
            new_nodes.append(TextNode(current_text, text_type=TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        links = extract_markdown_links(old_node.text)
        if not links:
            new_nodes.append(old_node)
            continue

        current_text = old_node.text
        for link in links:
            parts = current_text.split(f"[{link[0]}]({link[1]})", 1)
            if parts[0] != "":
                new_nodes.append(TextNode(parts[0], text_type=TextType.TEXT))
            new_nodes.append(TextNode(link[0], text_type=TextType.LINK, url=link[1]))
            current_text = parts[1]
        if current_text:
            new_nodes.append(TextNode(current_text, text_type=TextType.TEXT))
    return new_nodes


def split_nodes_quotes(nodes):
    new_nodes = []
    for node in nodes:
        if node.text_type == TextType.TEXT:
            lines = node.text.split("\n")
            quote_lines = []
            other_lines = []
            for line in lines:
                if line.startswith('>'):
                    quote_lines.append(line.lstrip('> ').strip())
                else:
                    other_lines.append(line)
            if quote_lines:
                quote_text = ' '.join(quote_lines)
                new_nodes.append(TextNode(quote_text, text_type=TextType.TEXT))
            if other_lines:
                other_text = '\n'.join(other_lines)
                new_nodes.append(TextNode(other_text, text_type=TextType.TEXT))
        else:
            new_nodes.append(node)
    return new_nodes


def text_to_textnodes(text):
    if text == "":
        return [TextNode("", text_type=TextType.TEXT)]

    nodes = [TextNode(text, text_type=TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_quotes(nodes)
    nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, '_', TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
    return nodes
