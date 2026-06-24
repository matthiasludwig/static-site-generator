import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_init(self):
        node = HTMLNode(tag="div", value="Hello", children=[], props={"class": "my-class"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"class": "my-class"})

    def test_props_to_html(self):
        node1 = HTMLNode(tag="div", props={"class": "my-class", "id": "my-id"})
        self.assertEqual(node1.props_to_html(), ' class="my-class" id="my-id"')

        node2 = HTMLNode(tag="span", props=None)
        self.assertEqual(node2.props_to_html(), "")

        node3 = HTMLNode(tag="p", props={})
        self.assertEqual(node3.props_to_html(), "")