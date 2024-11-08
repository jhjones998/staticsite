import re

from enum import Enum
from typing import Optional

from leafnode import LeafNode
from parentnode import ParentNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: Optional[str] = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: "TextNode") -> bool:
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )
    
    def __repr__(self) -> str:
        return f"TextNode({self.text=}, {self.text_type.value=}, {self.url=})"


TEXTTYPE_TO_DELIMITERS = {
    TextType.BOLD: "**",
    TextType.ITALIC: "*",
    TextType.CODE: "`",
}


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            if not text_node.url:
                raise ValueError("Link text node must have a URL")
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            if not text_node.url:
                raise ValueError("Image text node must have a URL")
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})


def block_to_parent_node(block: str, block_type: BlockType) -> ParentNode:
    block = block.strip()
    if block_type == BlockType.PARAGRAPH:
        return ParentNode("p", [text_node_to_html_node(node) for node in text_to_textnodes(block)], None)
    elif block_type == BlockType.HEADING:
        level = block.split(" ")[0].count("#")
        return ParentNode(f"h{level}", [text_node_to_html_node(node) for node in text_to_textnodes(block[level + 1:])], None)
    elif block_type == BlockType.CODE:
        return ParentNode("pre", [ParentNode("code", [text_node_to_html_node(node) for node in text_to_textnodes(block[3:-3])], None)], None)
    elif block_type == BlockType.QUOTE:
        return ParentNode("blockquote", [text_node_to_html_node(node) for node in text_to_textnodes(block[2:].replace("\n> ", "\n"))], None)
    elif block_type == BlockType.UNORDERED_LIST:
        return ParentNode("ul", [ParentNode("li", [text_node_to_html_node(node) for node in text_to_textnodes(line[2:])], None) for line in block.split("\n")], None)
    elif block_type == BlockType.ORDERED_LIST:
        return ParentNode("ol", [ParentNode("li", [text_node_to_html_node(node) for node in text_to_textnodes(line[3:])], None) for line in block.split("\n")], None)
    raise ValueError("Invalid block type")


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        # This assumes that we're using standard markdown delimiters, will not work for generic delimiters
        parts = re.split(rf'(?<!{re.escape(delimiter[-1])}){re.escape(delimiter)}(?!{re.escape(delimiter[0])})', node.text)
        if len(parts) != 1 and len(parts) % 2 == 0:
            raise ValueError("Unclosed delimiter")
        for i, part in enumerate(parts):
            if part:
                if i % 2 == 0:
                    new_nodes.append(TextNode(part, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(part, text_type))
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str]]:
    return re.findall(r"(!\[(.*?)\]\((.+?)\))", text)


def extract_markdown_links(text: str) -> list[tuple[str]]:
    return re.findall(r"((?<!\!)\[(.*?)\]\((.+?)\))", text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue
        leftovers = node.text
        for image in images:
            split_node_text = leftovers.split(image[0], 1)
            new_nodes.append(TextNode(split_node_text[0], TextType.TEXT))
            new_nodes.append(TextNode(image[1], TextType.IMAGE, image[2]))
            leftovers = split_node_text[1]
        if leftovers:
            new_nodes.append(TextNode(leftovers, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue
        leftovers = node.text
        for link in links:
            split_node_text = leftovers.split(link[0], 1)
            new_nodes.append(TextNode(split_node_text[0], TextType.TEXT))
            new_nodes.append(TextNode(link[1], TextType.LINK, link[2]))
            leftovers = split_node_text[1]
        if leftovers:
            new_nodes.append(TextNode(leftovers, TextType.TEXT))
    return new_nodes


def markdown_to_blocks(markdown: str) -> list[str]:
    return [block.strip() for block in markdown.split("\n\n") if block.strip()]


def block_to_block_type(block: str) -> BlockType:
    block = block.strip()
    if block.startswith("#"):
        if '# ' not in block[:7]:
            raise ValueError("Invalid heading block")
        return BlockType.HEADING
    elif block.startswith("```"):
        if not block.endswith("```"):
            raise ValueError("Invalid code block")
        return BlockType.CODE
    elif block.startswith(">"):
        for line in block.split("\n"):
            if not line.startswith(">"):
                raise ValueError("Invalid quote block")
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in block.split("\n"):
            if not line.startswith("- "):
                raise ValueError("Invalid unordered list block")
        return BlockType.UNORDERED_LIST
    if block.startswith("* "):
        for line in block.split("\n"):
            if not line.startswith("* "):
                raise ValueError("Invalid unordered list block")
        return BlockType.UNORDERED_LIST
    if block[0].isdigit():
        for line in block.split("\n"):
            if not line[0].isdigit() or line[1:3] != ". ":
                raise ValueError("Invalid ordered list block")
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def text_to_textnodes(text: str) -> list[TextNode]:
    node = TextNode(text, TextType.TEXT)
    parts = [node]
    for text_type in TextType:
        if text_type == TextType.TEXT:
            continue
        if text_type in {TextType.BOLD, TextType.ITALIC, TextType.CODE}:
            parts = split_nodes_delimiter(parts, TEXTTYPE_TO_DELIMITERS[text_type], text_type)
        elif text_type == TextType.IMAGE:
            parts = split_nodes_image(parts)
        elif text_type == TextType.LINK:
            parts = split_nodes_link(parts)
    return parts

