import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = HTMLNode("p", "Hello, world!")
        node2 = HTMLNode("p", "Hello, world!")
        self.assertEqual(node1, node2)

    def test_not_eq(self):
        node3 = HTMLNode("p", "Hello, world!")
        node4 = HTMLNode("h1", "Hello, world!")
        self.assertNotEqual(node3, node4)

    def test_leaf_eq(self):
        node5 = LeafNode("p", "Hello, world!")
        node6 = LeafNode("p", "Hello, world!")
        self.assertEqual(node5, node6)

    def test_leaf_not_eq(self):
        node7 = LeafNode("p", "Hello, world!")
        node8 = LeafNode("h1", "Hello, world!")
        self.assertNotEqual(node7, node8)

    def test_leaf_to_html_p(self):
        node9 = LeafNode("p", "Hello, world!")
        self.assertEqual(node9.to_html(), "<p>Hello, world!</p>")

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

if __name__ == "__main__":
    unittest.main()
