from typing import Optional
from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag: Optional[str], children: list[HTMLNode], props: Optional[dict[str, str]]) -> None:
        super().__init__(tag, None, children, props)
    
    def __repr__(self) -> str:
        return f"ParentNode({self.tag=}, {self.children=}, {self.props=})"
    
    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("ParentNode must have a tag")
        if not self.children:
            raise ValueError("ParentNode must have children")
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"