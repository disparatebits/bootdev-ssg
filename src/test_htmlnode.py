import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("a", "example.com", props={"href": "https://www.google.com", "target": "_blank", })
        expected = 'href="https://www.google.com" target="_blank" '
        self.assertEqual(expected, node.props_to_html())

    def test_eq(self):
        node = HTMLNode("This is a text node", )
        node2 = HTMLNode("This is a text node", )
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = HTMLNode("This is a text node", )
        different_node = HTMLNode("node")
        self.assertNotEqual(node, different_node)


class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node1 = LeafNode("p", "Hello, test!")
        node2 = LeafNode("p", "Hello, test!")
        self.assertEqual(node1, node2)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_pre(self):
        node = LeafNode("pre", "Hello, World!\nThis is a test.")
        expected_output = "<pre>Hello, World!\nThis is a test.</pre>"
        self.assertEqual(node.to_html(), expected_output)

    def test_leaf_to_html_em(self):
        node = LeafNode("em", "Emphasis mine")
        expected_output = "<em>Emphasis mine</em>"
        self.assertEqual(node.to_html(), expected_output)


class TestParentNode(unittest.TestCase):
    def test_print_html(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        expected = "<div><span>child</span></div>"
        self.assertEqual(expected, parent_node.to_html())

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_no_children_raises_error(self):
        with self.assertRaises(ValueError):
            parent_node = ParentNode("div", [None])
            parent_node.to_html()

    def test_deep_nesting(self):
        leaf = LeafNode("b", "text")
        parent1 = ParentNode("p", [leaf])
        parent2 = ParentNode("div", [parent1])
        parent3 = ParentNode("section", [parent2])
        self.assertEqual(parent3.to_html(), "<section><div><p><b>text</b></p></div></section>")

    def test_empty_children_list(self):
        parent = ParentNode("div", [])
        self.assertEqual(parent.to_html(), "<div></div>")

if __name__ == "__main__":
    unittest.main()
