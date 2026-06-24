import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_init(self):
        node = LeafNode(tag="leaf", value="Leaf Node", props={"data": "value"})
        self.assertEqual(node.tag, "leaf")
        self.assertEqual(node.value, "Leaf Node")
        self.assertEqual(node.props, {"data": "value"})

    def test_props_to_html(self):
        node1 = LeafNode(tag="leaf", props={"data": "value", "id": "leaf-id"}, value="Hello")
        self.assertEqual(node1.props_to_html(), ' data="value" id="leaf-id"')

        node2 = LeafNode(tag="leaf", props=None, value="Hello")
        self.assertEqual(node2.props_to_html(), "")

        node3 = LeafNode(tag="leaf", props={}, value="Hello")
        self.assertEqual(node3.props_to_html(), "")

        node = LeafNode(tag="p", value="Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")