from typing import List, Dict, Optional


class HTMLNode:
    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        children: Optional[List["HTMLNode"]] = None,
        props: Optional[Dict[str, str]] = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self) -> str:
        raise NotImplementedError("This method should be implemented by subclasses")

    def props_to_html(self) -> str:
        if not self.props:
            return ""
        return " " + " ".join(f'{key}="{value}"' for key, value in self.props.items())

    def __repr__(self) -> str:
        return f"HTMLNode(tag={self.tag!r}, value={self.value!r}, children={self.children!r}, props={self.props!r})"


class LeafNode(HTMLNode):
    def __init__(
        self, tag: Optional[str], value: str, props: Optional[Dict[str, str]] = None
    ):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self) -> str:
        if not self.value:
            raise ValueError("LeafNode must have a value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, LeafNode):
            return NotImplemented
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.props == other.props
        )

    def __repr__(self) -> str:
        return f"LeafNode(tag={self.tag!r}, value={self.value!r}, props={self.props!r})"


class ParentNode(HTMLNode):
    def __init__(
        self, tag: str, children: List[HTMLNode], props: Optional[Dict[str, str]] = None
    ):
        if not tag:
            raise ValueError("ParentNode must have a tag")
        if not children:
            raise ValueError("ParentNode must have children")
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("ParentNode must have a tag")
        if not self.children:
            raise ValueError("ParentNode must have children")
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __repr__(self) -> str:
        return f"ParentNode(tag={self.tag!r}, children={self.children!r}, props={self.props!r})"
