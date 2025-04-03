import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, \
    extract_markdown_links, text_to_textnodes


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        different_node = TextNode("This is a text node", TextType.LINK, "https://example.com")
        self.assertNotEqual(node, different_node)

    def test_url_is_none(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.url, None)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_invalid_text_type(self):
        with self.assertRaises(Exception):
            node = TextNode("This is a text node", TextType.INVALID)
            text_node_to_html_node(node)

    def test_link_text_node(self):
        node = TextNode("This is a link", TextType.LINK, 'https://example.com')
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, 'This is a link')
        self.assertEqual(html_node.props, {'href': 'https://example.com'})

    def test_split_node_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_delimiter_multiple_pairs(self):
        node = TextNode("**Bold** normal **more bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        assert len(new_nodes) == 3

    def test_split_nodes_delimiter_empty_strings(self):
        node = TextNode("**Bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        assert len(new_nodes) == 1
        assert new_nodes[0].text == "Bold"
        assert new_nodes[0].text_type == TextType.BOLD

    def test_split_nodes_delimiter_missing(self):
        with self.assertRaises(Exception):
            node = TextNode("**Forgot a delimiter!", TextType.TEXT)
            split_nodes_delimiter([node], "**", TextType.BOLD)


    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_markdown_links_special_chars(self):
        matches = extract_markdown_links(
            "[Text with spaces & symbols!](https://example.com/path?query=value)"
        )
        self.assertListEqual([
            ("Text with spaces & symbols!", "https://example.com/path?query=value")
        ], matches)

    def test_text_to_textnodes_empty(self):
        result = text_to_textnodes("")
        expected = [TextNode("", TextType.TEXT)]
        assert result == expected


if __name__ == "__main__":
    unittest.main()
