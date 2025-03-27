import unittest

from htmlnode import HTMLNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = HTMLNode("p", "Hello, world!")
        node2 = HTMLNode("p", "Hello, world!")
        self.assertEqual(node1, node2)

    def test_not_eq(self):
        node3 = HTMLNode("p", "Hello, world!")
        node4 = HTMLNode("h1", "Hello, world!")
        self.assertNotEqual(node3, node4)

if __name__ == "__main__":
    unittest.main()
