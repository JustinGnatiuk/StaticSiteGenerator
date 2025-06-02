
# Main HTML Node

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value 
        self.children = children if children is not None else []
        self.props = props if props is not None else {}
    
    def __eq__(self, otherNode):
        return (

            (self.tag == otherNode.tag) and 
            (self.value == otherNode.value) and 
            (sorted(self.children) == sorted(otherNode.children)) and 
            (self.props == otherNode.props)
        )
                
    
    def to_html(self):
        raise NotImplemented("HTMLNode not implemented, are you calling this on the right object?")
    
    def props_to_html(self):

        if not self.props:
            return ""

        return " " + " ".join(f'{key}="{value}"' for key, value in self.props.items())

    def __repr__(self):

        return_string = f"Tag: {self.tag}\nValue: {self.value}\n"

        if self.children:
            for child in self.children:
                return_string += f"Child: {child}\n"
        if self.props:      
            for key, value in self.props.items():
                return_string += f"Property {key}={value}\n"
        
        return return_string
        
# Child Leaf Node
class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):

        super().__init__(tag, value, None, props)
        
        if value == None:
            raise ValueError("All leaf nodes must have a value")
    
    def __repr__(self):

        return_string = f"Tag: {self.tag}\nValue: {self.value}\n"

        if self.props:      
            for key, value in self.props.items():
                return_string += f"Property {key}={value}\n"
        
        return return_string

    def to_html(self):
        
        if self.tag == None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


# Parent Node
class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):

        super().__init__(tag=tag, value=None, children=children, props=props)

        if tag == None:
            raise ValueError("Parent node must have a tag")
        if children == None:
            raise ValueError("Parent node must have children")

    def __repr__(self):
        
        return_string = f"Tag: {self.tag}\nChildren:\n"


        return_string += f"[\n"
        for child in self.children:
            if isinstance(child, LeafNode):
                return_string += f"Tag:{child.tag} Value:{child.value},\n"
            elif isinstance(child, ParentNode):
                return_string += child.__repr__()
        return_string += f"]\n"

        if self.props:      
            for key, value in self.props.items():
                return_string += f"Property {key}={value}\n"
        
        return return_string

    def to_html(self):
        
        return_string = ""

        for child in self.children:
            return_string += child.to_html()
        
        return f"<{self.tag}>{return_string}</{self.tag}>"