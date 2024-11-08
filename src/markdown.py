from textnode import block_to_parent_node, block_to_block_type, markdown_to_blocks
from parentnode import ParentNode


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        block = block.strip()
        block_type = block_to_block_type(block)
        nodes.append(block_to_parent_node(block, block_type))
    return ParentNode("div", nodes, None)


def extract_title(markdown: str) -> str:
    blocks = markdown_to_blocks(markdown)
    if not blocks:
        raise Exception("No blocks found in markdown")
    title = blocks[0]
    if title.startswith("# "):
        return title[2:]
    raise Exception("No title found in markdown")
