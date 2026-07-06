from enum import Enum

from htmlnode import HTMLNode
from parentnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
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
    

def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)

    WrappingNode = ParentNode(tag="div", children=[])

    for block in blocks:
        block_type = block_to_block_type(block)

        tag = None # To store the tag value for the HTMLParent
        HTMLParent = None # To store the ParentNode for the current block

        if block_type == BlockType.HEADING:
            heading_len = len(re.match(r"^(#+)\s", block).group(1))
            tag = "h" + str(heading_len)
            HTMLParent = ParentNode(tag=tag, children=text_to_children(block[heading_len + 1:]))
        elif block_type == BlockType.UNORDERED_LIST:
            tag = "ul"
            items = block.split("\n")
            li_nodes = []
            for i in items:
                text = i[2:]  # Remove the "- " prefix
                li_nodes.append(ParentNode(tag="li", children=text_to_children(text)))
            HTMLParent = ParentNode(tag=tag, children=li_nodes)
        elif block_type == BlockType.ORDERED_LIST:
            tag = "ol"
            items = block.split("\n")
            ol_nodes = []
            for i in items:
                text = i.split(". ",1)[1]  # Remove the "1. " prefix (or any number followed by ". ")
                ol_nodes.append(ParentNode(tag="li", children=text_to_children(text)))
            HTMLParent = ParentNode(tag=tag, children=ol_nodes)
        elif block_type == BlockType.QUOTE:
            tag = "blockquote"
            items = block.split("\n")
            quote_text = []
            for i in items:
                text = i[2:]  # Remove the "> " prefix
                quote_text.append(text)
            blockquote_text = "\n".join(quote_text)
            HTMLParent = ParentNode(tag=tag, children=text_to_children(blockquote_text))
        elif block_type == BlockType.CODE:
            tag = "pre"
            raw_text_node = TextNode(text=block[3:-3].lstrip('\n'), text_type=TextType.TEXT)
            child = text_node_to_html_node(raw_text_node)
            code_node = ParentNode(tag="code", children=[child])
            HTMLParent = ParentNode(tag=tag, children=[code_node])
        elif block_type == BlockType.PARAGRAPH:
            tag = "p"
            HTMLParent = ParentNode(tag=tag, children=text_to_children(block))
        WrappingNode.children.append(HTMLParent)

    return WrappingNode


def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    children = [text_node_to_html_node(node) for node in text_nodes]
    return children