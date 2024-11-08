from typing import Optional
from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag: Optional[str], value: Optional[str], props: Optional[dict[str, str]] = None) -> None:
        super().__init__(tag, value, None, props)

    def __repr__(self) -> str:
        return f"LeafNode({self.tag=}, {self.value=}, {self.props=})"
    
    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value or ''}</{self.tag}>"
