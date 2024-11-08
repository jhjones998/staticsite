import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_repr(self):
        node = LeafNode("p", "This is a paragraph", {"class": "paragraph"})
        self.assertEqual(repr(node), "LeafNode(self.tag='p', self.value='This is a paragraph', self.props={'class': 'paragraph'})")

    def test_to_html(self):
        node = LeafNode("p", "This is a paragraph", {"class": "paragraph", "style": "color: red"})
        self.assertEqual(node.to_html(), '<p class="paragraph" style="color: red">This is a paragraph</p>')
    
    def test_to_html_empty_props(self):
        node = LeafNode("p", "This is a paragraph", {})
        self.assertEqual(node.to_html(), '<p>This is a paragraph</p>')

    def test_to_html_none_props(self):
        node = LeafNode("p", "This is a paragraph", None)
        self.assertEqual(node.to_html(), '<p>This is a paragraph</p>')

    def test_to_html_none_value(self):
        self.assertRaises(ValueError, LeafNode("p", None, {"class": "paragraph"}).to_html)
    
    def test_to_html_none_tag(self):
        node = LeafNode(None, "This is a paragraph", {"class": "paragraph"})
        self.assertEqual(node.to_html(), 'This is a paragraph')


if __name__ == "__main__":
    unittest.main()
