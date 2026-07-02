import unittest
from helper import split_nodes_delimiter
from textnode import TextNode, TextType

class TestHelperMethods(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        # Test case 1: Basic splitting
        nodes = [TextNode("Hello,World", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, ",", TextType.TEXT)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "Hello")
        self.assertEqual(result[1].text, "World")

        # Test case 2: No delimiter present
        nodes = [TextNode("Hello World", TextType.TEXT)]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(nodes, ",", TextType.TEXT)

        # Test case 3: Different text type
        nodes = [TextNode("Hello,World", TextType.BOLD)]
        result = split_nodes_delimiter(nodes, ",", TextType.BOLD)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "Hello")
        self.assertEqual(result[1].text, "World")