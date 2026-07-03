import unittest
from helper import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
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

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

        def test_split_images(self):
            node = TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
                TextType.TEXT,
            )
            new_nodes = split_nodes_image([node])
            self.assertListEqual(
                [
                    TextNode("This is text with an ", TextType.TEXT),
                    TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                    TextNode(" and another ", TextType.TEXT),
                    TextNode(
                        "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                    ),
                ],
                new_nodes,
            )