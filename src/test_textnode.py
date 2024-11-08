import unittest

from textnode import (
    BlockType,
    TextNode, 
    TextType, 
    text_node_to_html_node, 
    split_nodes_delimiter, 
    extract_markdown_images, 
    extract_markdown_links, 
    split_nodes_image, 
    split_nodes_link,
    text_to_textnodes,
    markdown_to_blocks,
    block_to_block_type,
    block_to_parent_node
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_eq_when_different(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://google.com")
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_when_url_not_none(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://google.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://google.com")
        self.assertEqual(node, node2)
    
    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(repr(node), "TextNode(self.text='This is a text node', self.text_type.value='bold', self.url=None)")

    def test_repr_with_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://google.com")
        self.assertEqual(repr(node), "TextNode(self.text='This is a text node', self.text_type.value='bold', self.url='https://google.com')")

    def test_text_node_to_html_node_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(text_node_to_html_node(node).to_html(), "This is a text node")
    
    def test_text_node_to_html_node_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(text_node_to_html_node(node).to_html(), "<b>This is a text node</b>")
    
    def test_text_node_to_html_node_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(text_node_to_html_node(node).to_html(), "<i>This is a text node</i>")
    
    def test_text_node_to_html_node_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        self.assertEqual(text_node_to_html_node(node).to_html(), "<code>This is a text node</code>")
    
    def test_text_node_to_html_node_link(self):
        node = TextNode("This is a text node", TextType.LINK, "https://google.com")
        self.assertEqual(text_node_to_html_node(node).to_html(), '<a href="https://google.com">This is a text node</a>')
    
    def test_text_node_to_html_node_link_no_url(self):
        node = TextNode("This is a text node", TextType.LINK)
        self.assertRaises(ValueError, text_node_to_html_node, node)

    def test_text_node_to_html_node_image(self):
        node = TextNode("This is a text node", TextType.IMAGE, "https://google.com")
        self.assertEqual(text_node_to_html_node(node).to_html(), '<img src="https://google.com" alt="This is a text node"></img>')
    
    def test_text_node_to_html_node_image_no_url(self):
        node = TextNode("This is a text node", TextType.IMAGE)
        self.assertRaises(ValueError, text_node_to_html_node, node)

    def test_split_nodes_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "*", TextType.BOLD), 
            [node]
        )
    
    def test_split_nodes_bold(self):
        node = TextNode("This is a **bold** text node", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "**", TextType.BOLD), 
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text node", TextType.TEXT),
            ]
        )
    
    def test_split_nodes_italic(self):
        node = TextNode("This is a *italic* text node", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "*", TextType.ITALIC), 
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text node", TextType.TEXT),
            ]
        )

    def test_split_nodes_code(self):
        node = TextNode("This is a `code` text node", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "`", TextType.CODE), 
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" text node", TextType.TEXT),
            ]
        )

    def test_split_nodes_unclosed_delimiter(self):
        node = TextNode("This is a `code text node", TextType.TEXT)
        self.assertRaises(ValueError, split_nodes_delimiter, [node], "`", TextType.CODE)

    def test_split_nodes_startswith_delimiter(self):
        node = TextNode("`This is a code text` node", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "`", TextType.CODE), 
            [
                TextNode("This is a code text", TextType.CODE),
                TextNode(" node", TextType.TEXT),
            ]
        )
    
    def test_split_nodes_endswith_delimiter(self):
        node = TextNode("This is a code text `node`", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "`", TextType.CODE), 
            [
                TextNode("This is a code text ", TextType.TEXT),
                TextNode("node", TextType.CODE),
            ]
        )
    
    def test_split_nodes_is_delimiter(self):
        node = TextNode("`This is a code text node`", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "`", TextType.CODE), 
            [TextNode("This is a code text node", TextType.CODE)]
        )

    def test_split_nodes_multiple_delimiters(self):
        node = TextNode("This is a **bold** and *italic* text node", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "*", TextType.ITALIC), 
            [
                TextNode("This is a **bold** and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text node", TextType.TEXT),
            ]
        )

    def test_split_nodes_empty_delimiter(self):
        node = TextNode("This is a **** text node", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "**", TextType.BOLD), 
            [
                TextNode("This is a **** text node", TextType.TEXT),
            ]
        )
    
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(
            extract_markdown_images(text),
            [
                ("![rick roll](https://i.imgur.com/aKaOqIh.gif)", "rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", "obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
            ]
        )
    
    def test_extract_markdown_images_no_match(self):
        text = "This is text with a [link](https://google.com)"
        self.assertEqual(extract_markdown_images(text), [])

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://google.com) and [another link](https://bing.com)"
        self.assertEqual(
            extract_markdown_links(text),
            [
                ("[link](https://google.com)", "link", "https://google.com"),
                ("[another link](https://bing.com)", "another link", "https://bing.com")
            ]
        )
    
    def test_extract_markdown_links_no_match(self):
        text = "This is text with a ![image](https://i.imgur.com/aKaOqIh.gif)"
        self.assertEqual(extract_markdown_links(text), [])

    
    def test_split_nodes_image(self):
        node = TextNode("This is text with a ![image](https://i.imgur.com/aKaOqIh.gif) and a [link](https://google.com)", TextType.TEXT)
        split_nodes = split_nodes_image([node])
        self.assertEqual(
            split_nodes, 
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                TextNode(" and a [link](https://google.com)", TextType.TEXT),
            ]
        )

    def test_split_nodes_image_no_match(self):
        node = TextNode("This is text with a [link](https://google.com)", TextType.TEXT)
        split_nodes = split_nodes_image([node])
        self.assertEqual(
            split_nodes, 
            [node]
        )

    def test_split_nodes_link(self):
        node = TextNode("This is text with a ![image](https://i.imgur.com/aKaOqIh.gif) and a [link](https://google.com)", TextType.TEXT)
        split_nodes = split_nodes_link([node])
        self.assertEqual(
            split_nodes, 
            [
                TextNode("This is text with a ![image](https://i.imgur.com/aKaOqIh.gif) and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://google.com"),
            ]
        )

    def test_split_nodes_link_no_match(self):
        node = TextNode("This is text with a ![image](https://i.imgur.com/aKaOqIh.gif)", TextType.TEXT)
        split_nodes = split_nodes_link([node])
        self.assertEqual(
            split_nodes, 
            [node]
        )
    
    def test_text_to_textnodes(self):
        node = TextNode(
            "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)", 
            TextType.TEXT
        )
        self.assertEqual(
            text_to_textnodes(node.text),
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        )

    def test_text_to_textnodes_no_markdown(self):
        node = TextNode("This is text with no markdown", TextType.TEXT)
        self.assertEqual(
            text_to_textnodes(node.text),
            [node]
        )
    
    def test_text_to_textnodes_empty(self):
        node = TextNode("", TextType.TEXT)
        self.assertEqual(
            text_to_textnodes(node.text),
            []
        )
    
    def test_text_to_textnodes_only_markdown(self):
        node = TextNode("**bold** *italic* `code` ![image](https://i.imgur.com/fJRm4Vk.jpeg) [link](https://boot.dev)", TextType.TEXT)
        self.assertEqual(
            text_to_textnodes(node.text),
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        )
    
    def test_text_to_textnodes_unclosed_markdown(self):
        self.assertRaises(ValueError, text_to_textnodes, "This is **bold *italic* text")

    def test_markdown_to_blocks(self):
        text = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
            
        self.assertEqual(
            markdown_to_blocks(text),
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
            ]
        )
    
    def test_markdown_to_blocks_empty(self):
        text = ""
        self.assertEqual(
            markdown_to_blocks(text),
            []
        )
    
    def test_markdown_to_blocks_no_blocks(self):
        text = "This is a single block of text"
        self.assertEqual(
            markdown_to_blocks(text),
            [text]
        )
    
    def test_markdown_to_blocks_extra_newlines(self):
        text = "This is a single block of text\n\n\n\n"
        self.assertEqual(
            markdown_to_blocks(text),
            [text[:-4]]
        )
    
    def test_block_to_block_type(self):
        self.assertEqual(
            block_to_block_type("# This is a heading"),
            BlockType.HEADING
        )
        self.assertEqual(
            block_to_block_type("```python\nprint('Hello, World!')\n```"),
            BlockType.CODE
        )
        self.assertEqual(
            block_to_block_type("> This is a block quote\n> This is another block quote"),
            BlockType.QUOTE
        )
        self.assertEqual(
            block_to_block_type("1. This is a list item\n2. This is another list item"),
            BlockType.ORDERED_LIST
        )
        self.assertEqual(
            block_to_block_type("- This is a list item\n- This is another list item"),
            BlockType.UNORDERED_LIST
        )
        self.assertEqual(
            block_to_block_type("* This is a list item\n* This is another list item"),
            BlockType.UNORDERED_LIST
        )
        self.assertEqual(
            block_to_block_type("This is a paragraph of text"),
            BlockType.PARAGRAPH
        )
    
    def test_block_to_block_type_invalid_heading(self):
        self.assertRaises(ValueError, block_to_block_type, "#This is an invalid heading")
    
    def test_block_to_block_type_invalid_code(self):
        self.assertRaises(ValueError, block_to_block_type, "```python\nprint('Hello, World!')")
    
    def test_block_to_block_type_invalid_quote(self):
        self.assertRaises(ValueError, block_to_block_type, "> This is a block quote\nThis is an invalid block quote")
    
    def test_block_to_block_type_invalid_ordered_list(self):
        self.assertRaises(ValueError, block_to_block_type, "1 This is a list item\n2 This is another list item")
    
    def test_block_to_block_type_invalid_unordered_list(self):
        self.assertRaises(ValueError, block_to_block_type, "- This is a list item\nThis is an invalid list item")
    
    def test_block_to_block_type_invalid_unordered_list_asterisk(self):
        self.assertRaises(ValueError, block_to_block_type, "* This is a list item\nThis is an invalid list item")

    def test_block_to_parent_node_heading(self):
        block = "# This is a heading"
        self.assertEqual(
            block_to_parent_node(block, BlockType.HEADING).to_html(),
            "<h1>This is a heading</h1>"
        )
    
    def test_block_to_parent_node_code(self):
        block = "```python\nprint('Hello, World!')```"
        self.assertEqual(
            block_to_parent_node(block, BlockType.CODE).to_html(),
            "<pre><code>python\nprint('Hello, World!')</code></pre>"
        )
    
    def test_block_to_parent_node_quote(self):
        block = "> This is a block quote\n> This is another block quote"
        self.assertEqual(
            block_to_parent_node(block, BlockType.QUOTE).to_html(),
            "<blockquote>This is a block quote\nThis is another block quote</blockquote>"
        )
    
    def test_block_to_parent_node_ordered_list(self):
        block = "1. This is a list item\n2. This is another list item"
        self.assertEqual(
            block_to_parent_node(block, BlockType.ORDERED_LIST).to_html(),
            "<ol><li>This is a list item</li><li>This is another list item</li></ol>"
        )
    
    def test_block_to_parent_node_unordered_list(self):
        block = "- This is a list item\n- This is another list item"
        self.assertEqual(
            block_to_parent_node(block, BlockType.UNORDERED_LIST).to_html(),
            "<ul><li>This is a list item</li><li>This is another list item</li></ul>"
        )
    
    def test_block_to_parent_node_paragraph(self):
        block = "This is a paragraph of text"
        self.assertEqual(
            block_to_parent_node(block, BlockType.PARAGRAPH).to_html(),
            "<p>This is a paragraph of text</p>"
        )

    
if __name__ == "__main__":
    unittest.main()
