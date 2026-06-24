from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value:str, props: dict[str, str] | None = None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self) -> str:
        props_html = self.props_to_html()
        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"