from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type == text_type:
            if delimiter not in node.text:
                raise ValueError(f"Delimiter '{delimiter}' not found in text: {node.text}")
            parts = node.text.split(delimiter)
            new_nodes.extend([TextNode(part, text_type) for part in parts])
    
    return new_nodes