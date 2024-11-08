import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("p", "This is a paragraph", [], {"class": "paragraph"})
        self.assertEqual(repr(node), "HTMLNode(self.tag='p', self.value='This is a paragraph', self.children=[], self.props={'class': 'paragraph'})")
    
    def test_props_to_html(self):
        node = HTMLNode("p", "This is a paragraph", [], {"class": "paragraph", "href": "https://google.com"})
        self.assertEqual(node.props_to_html(), ' class="paragraph" href="https://google.com"')
    
    def test_props_to_html_empty(self):
        node = HTMLNode("p", "This is a paragraph", [], {})
        self.assertEqual(node.props_to_html(), "")
    
    def test_props_to_html_none(self):
        node = HTMLNode("p", "This is a paragraph", [], None)
        self.assertEqual(node.props_to_html(), "")

    def test_to_html(self):
        self.assertRaises(NotImplementedError, HTMLNode("p", "This is a paragraph", [], {"class": "paragraph"}).to_html)


if __name__ == "__main__":
    unittest.main()
