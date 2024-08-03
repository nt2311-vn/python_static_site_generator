from typing import Optional, List, Dict


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
        raise NotImplementedError("This method should be implemented by subclass")

    def props_to_html(self) -> str:
        if not self.props:
            return ""

        return " " + " ".join(f'{key}="{value}"' for key, value in self.props.items())

    def __repr__(self) -> str:
        return f"HTMLNode(tag={self.tag!r}), value={self.value!r}, children={self.children!r}, props={self.props!r}"
