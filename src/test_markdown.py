import unittest

from markdown import markdown_to_html_node, extract_title


class TestMarkdownConversion(unittest.TestCase):
    def test_markdown_to_html_node(self):
        markdown = """# Header 1

## Header 2

### Header 3

#### Header 4

##### Header 5

###### Header 6"""
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(
            html_node.to_html(),
            """<div><h1>Header 1</h1><h2>Header 2</h2><h3>Header 3</h3><h4>Header 4</h4><h5>Header 5</h5><h6>Header 6</h6></div>"""
        )

    def test_extract_title(self):
        markdown = """# Title"""
        title = extract_title(markdown)
        self.assertEqual(title, "Title")
    
    def test_extract_title_no_title(self):
        markdown = """No title"""
        with self.assertRaises(Exception):
            extract_title(markdown)
    
    def test_extract_title_empty(self):
        markdown = ""
        with self.assertRaises(Exception):
            extract_title(markdown)
    

    
if __name__ == "__main__":
    unittest.main()
