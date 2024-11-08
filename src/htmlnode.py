from typing import Optional


class HTMLNode:
    def __init__(
            self,
            tag: Optional[str] = None, 
            value: Optional[str] = None, 
            children: Optional[list["HTMLNode"]] = None,
            props: Optional[dict[str, str]] = None,
        ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag=}, {self.value=}, {self.children=}, {self.props=})"
    
    def to_html(self) -> str:
        raise NotImplementedError()

    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        props_string = " ".join(f'{key}="{value}"' for key, value in self.props.items())
        if props_string:
            props_string = f" {props_string}"
        return props_string
