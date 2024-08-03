from typing import Optional, List, Tuple
from htmlnode import LeafNode
import re


text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"


class TextNode:
    def __init__(self, text: str, text_type: str, url: Optional[str] = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TextNode):
            return False
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def extract_markdown_images(text: str) -> List[Tuple[str, str]]:
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return [(alt, url) for alt, url in matches]


def extract_markdown_links(text: str) -> List[Tuple[str, str]]:
    pattern = r"(?<!\!)\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return [(anchor_text, url) for anchor_text, url in matches]


def split_nodes_image(old_nodes: List[TextNode]) -> List[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue

        text = node.text
        images = extract_markdown_images(text)
        if not images:
            new_nodes.append(node)
            continue

        for alt, url in images:
            sections = text.split(f"![{alt}]({url})", 1)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(TextNode(alt, text_type_image, url))
            text = sections[1]
        if text:
            new_nodes.append(TextNode(text, text_type_text))

    return new_nodes


def split_nodes_link(old_nodes: List[TextNode]) -> List[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue

        text = node.text
        links = extract_markdown_links(text)
        if not links:
            new_nodes.append(node)
            continue

        for anchor_text, url in links:
            sections = text.split(f"[{anchor_text}]({url})", 1)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(TextNode(anchor_text, text_type_link, url))
            text = sections[1]
        if text:
            new_nodes.append(TextNode(text, text_type_text))

    return new_nodes


def text_to_textnodes(text: str) -> List[TextNode]:
    nodes = [TextNode(text, text_type_text)]

    # Split nodes based on delimiters
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)

    # Split nodes based on links and images
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)

    return nodes


def text_node_to_html_node(text_node):
    if text_node.text_type == "text":
        return LeafNode(tag=None, value=text_node.text)
    elif text_node.text_type == "bold":
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == "italic":
        return LeafNode(tag="i", value=text_node.text)
    elif text_node.text_type == "code":
        return LeafNode(tag="code", value=text_node.text)
    elif text_node.text_type == "link":
        if text_node.url is None:
            raise ValueError("Link TextNode must have a URL")
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    elif text_node.text_type == "image":
        if text_node.url is None:
            raise ValueError("Image TextNode must have a URL")
        return LeafNode(
            tag="img", value="", props={"src": text_node.url, "alt": text_node.text}
        )
    else:
        raise ValueError(f"Unknown text_type: {text_node.text_type}")


def split_nodes_delimiter(
    old_nodes: List[TextNode], delimiter: str, text_type: str
) -> List[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != "text":
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError(f"Unmatched delimiter '{delimiter}' in text: {node.text}")

        for i, part in enumerate(parts):
            if i % 2 == 0:
                if part:
                    new_nodes.append(TextNode(part, "text"))
            else:
                if part:
                    new_nodes.append(TextNode(part, text_type))

    return new_nodes
