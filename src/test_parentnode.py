import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_repr(self):
        node = ParentNode("div", [LeafNode("p", "This is a paragraph", {"class": "paragraph"})], {"class": "container"})
        self.assertEqual(repr(node), "ParentNode(self.tag='div', self.children=[LeafNode(self.tag='p', self.value='This is a paragraph', self.props={'class': 'paragraph'})], self.props={'class': 'container'})")

    def test_to_html_tag_none(self):
        self.assertRaises(ValueError, ParentNode(None, [LeafNode("p", "This is a paragraph", {"class": "paragraph"})], {"class": "container"}).to_html)
    
    def test_to_html_children_none(self):
        self.assertRaises(ValueError, ParentNode("div", None, {"class": "container"}).to_html)

    def test_to_html_children_empty(self):
        self.assertRaises(ValueError, ParentNode("div", [], {"class": "container"}).to_html)

    def test_to_html_only_leaf_nodes(self):
        node = ParentNode("div", [LeafNode("p", "This is a paragraph", {"class": "paragraph"}), LeafNode("p", "This is another paragraph", {"class": "paragraph"})], {"class": "container"})
        self.assertEqual(node.to_html(), '<div class="container"><p class="paragraph">This is a paragraph</p><p class="paragraph">This is another paragraph</p></div>')
    
    def test_to_html_leaf_and_parent_nodes(self):
        node = ParentNode("div", [LeafNode("p", "This is a paragraph", {"class": "paragraph"}), ParentNode("div", [LeafNode("p", "This is another paragraph", {"class": "paragraph"})], {"class": "container"})], {"class": "container"})
        self.assertEqual(node.to_html(), '<div class="container"><p class="paragraph">This is a paragraph</p><div class="container"><p class="paragraph">This is another paragraph</p></div></div>')

    def test_to_html_only_parent_nodes(self):
        node = ParentNode("div", [ParentNode("div", [LeafNode("p", "This is a paragraph", {"class": "paragraph"})], {"class": "container"}), ParentNode("div", [LeafNode("p", "This is another paragraph", {"class": "paragraph"})], {"class": "container"})], {"class": "container"})
        self.assertEqual(node.to_html(), '<div class="container"><div class="container"><p class="paragraph">This is a paragraph</p></div><div class="container"><p class="paragraph">This is another paragraph</p></div></div>')


if __name__ == "__main__":
    unittest.main()
