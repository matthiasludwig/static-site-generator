from textnode import TextNode, TextType
import re


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type == text_type:
            if delimiter not in node.text:
                raise ValueError(f"Delimiter '{delimiter}' not found in text: {node.text}")
            parts = node.text.split(delimiter)
            new_nodes.extend([TextNode(part, text_type) for part in parts])
    
    return new_nodes

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r'!\[(.*?)\]\((.*?)\)', text)
    return matches

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r'\[(.*?)\]\((.*?)\)', text)
    return matches

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        matches = extract_markdown_images(node.text)
        if matches:
            for match in matches:
                split_text = node.text.split(f'![{match[0]}]({match[1]})')
                new_nodes.extend([TextNode(part, TextType.TEXT) for part in split_text if part])
            new_nodes.append(TextNode(text=match[0], text_type=TextType.IMAGE, url=match[1]))

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        matches = extract_markdown_links(node.text)
        if matches:
            for match in matches:
                split_text = node.text.split(f'[{match[0]}]({match[1]})')
                new_nodes.extend([TextNode(part, TextType.TEXT) for part in split_text if part])
            new_nodes.append(TextNode(text=match[0], text_type=TextType.LINK, url=match[1]))
    return new_nodes
