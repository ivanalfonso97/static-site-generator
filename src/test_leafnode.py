import unittest

from leafnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = LeafNode("p", "Hello, world!")
        node2 = LeafNode("p", "Hello, world!")
        self.assertEqual(node1, node2)

    def test_not_eq(self):
        node3 = LeafNode("p", "Hello, world!")
        node4 = LeafNode("h1", "Hello, world!")
        self.assertNotEqual(node3, node4)

    def test_leaf_to_html_p(self):
        node5 = LeafNode("p", "Hello, world!")
        self.assertEqual(node5.to_html(), "<p>Hello, world!</p>")

if __name__ == "__main__":
    unittest.main()
