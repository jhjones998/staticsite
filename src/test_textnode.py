import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links


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
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
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
                ("link", "https://google.com"),
                ("another link", "https://bing.com")
            ]
        )
    
    def test_extract_markdown_links_no_match(self):
        text = "This is text with a ![image](https://i.imgur.com/aKaOqIh.gif)"
        self.assertEqual(extract_markdown_links(text), [])

    
if __name__ == "__main__":
    unittest.main()
