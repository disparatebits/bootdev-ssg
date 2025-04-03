class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ""
        html = ""
        for k, v in self.props.items():
            html += f"{k}=\"{v}\" "
        return html

    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children},{self.props_to_html()})"

    def props_to_string(self):
        if not self.props:
            return ""
        return " ".join(f'{k}="{v}"' for k, v in self.props.items())


class LeafNode(HTMLNode):
    def __init__(self, tag, value, children=None, props=None):
        super().__init__(tag=tag, value=value, props=props)
        if children is not None:
            raise ValueError('cannot have children')

    def to_html(self):
        if self.tag is None:
            return self.value
        if self.value is None:
            raise ValueError('value cannot be None')
        props_string = self.props_to_string()
        if props_string:
            return f"<{self.tag} {props_string}>{self.value}</{self.tag}>"
        return f"<{self.tag}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)
        if tag is None:
            raise ValueError('ParentNode tag cannot be None')
        if children is None:
            raise ValueError('ParentNode must have children')
        for child in self.children:
            if child is None:
                raise ValueError('ParentNode cannot have a NoneType child')

    def to_html(self):
        if not self.children:
            return f"<{self.tag}></{self.tag}>"
        html = ''
        for child in self.children:
            html += child.to_html()

        props_string = self.props_to_string()
        if props_string:
            return f"<{self.tag} {props_string}>{html or self.value}</{self.tag}>"
        return f"<{self.tag}>{html or self.value}</{self.tag}>"
