from enum import Enum
from htmlnode import *

class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMG = "image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, otherNode):
        return (self.text == otherNode.text) and (self.text_type == otherNode.text_type) and (self.url == otherNode.url)

    def __repr__(self):
        if self.url == None:
            return f"TextNode(\"{self.text}\", {self.text_type})"
        else:
            return f"TextNode(\"{self.text}\", {self.text_type}, {self.url})"

# Function to convert a text node into an HTML Leaf node
def text_node_to_html_node(text_node): 

    match text_node.text_type.value:
        case "normal":
            return LeafNode(None, text_node.text)
        case "bold":
            return LeafNode("b", text_node.text)
        case "italic":
            return LeafNode("i", text_node.text)
        case "code":
            return LeafNode("code", text_node.text)
        case "link":
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case "image":
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("text node does not have a known text type")