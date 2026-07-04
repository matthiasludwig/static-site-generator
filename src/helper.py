from enum import Enum

from textnode import TextNode, TextType
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

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
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        remaining_text = node.text

        matches = extract_markdown_images(node.text)
        if matches:
            for match in matches:
                split_text = remaining_text.split(f'![{match[0]}]({match[1]})', 1)
                if split_text[0] != "":
                    new_nodes.append(TextNode(split_text[0], TextType.TEXT))
                
                new_nodes.append(TextNode(text=match[0], text_type=TextType.IMAGE, url=match[1]))
                remaining_text = split_text[1] if len(split_text) > 1 else ""
            
            if remaining_text:
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
        else:
            new_nodes.append(node)

    
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        remaining_text = node.text

        matches = extract_markdown_links(node.text)
        if matches:
            for match in matches:
                split_text = remaining_text.split(f'[{match[0]}]({match[1]})', 1)
                if split_text[0] != "":
                    new_nodes.append(TextNode(split_text[0], TextType.TEXT))
                
                new_nodes.append(TextNode(text=match[0], text_type=TextType.LINK, url=match[1]))
                remaining_text = split_text[1] if len(split_text) > 1 else ""
            
            if remaining_text:
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
        else:
            new_nodes.append(node)

    
    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    text_nodes = []

    text_nodes = split_nodes_image([TextNode(text, TextType.TEXT)])
    text_nodes = split_nodes_link(text_nodes)

    return text_nodes

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    return [block.strip() for block in blocks if block.strip()]


def block_to_block_type(block: str) -> BlockType:
    if re.match(r"^#{1,6}\s", block):
        return BlockType.HEADING
    elif block.startswith("- "):
        return BlockType.UNORDERED_LIST
    elif re.match(r'^\d+\.\s', block):
        return BlockType.ORDERED_LIST
    elif block.startswith(">"):
        return BlockType.QUOTE
    elif block.startswith("```"):
        return BlockType.CODE
    else:
        return BlockType.PARAGRAPH