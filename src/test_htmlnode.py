
# Tests for HTMLNode class and child classes

import unittest
from colorama import Fore, Back, Style

from htmlnode import HTMLNode, LeafNode, ParentNode

# Test functionality of HTML Node classs
class TestHTMLNode(unittest.TestCase):

    def test_html_node_create(self):

        print(Fore.GREEN + "---------------------------------------------------------------")
        print(Fore.GREEN + "Creating HTML Nodes...")
        print(Fore.GREEN + "---------------------------------------------------------------")
        print(Style.RESET_ALL)

        print("Node 1:")
        node = HTMLNode("p", "This is a paragraph", None, None)
        print( node.__repr__() )

        print("Node 2:")
        node_props = {

                "href": "https://www.google.com",
                "target": "_blank",
            }

        node = HTMLNode("a", "This is a link", None, node_props)
        print( node.__repr__() )


    def test_eq(self):

        node = HTMLNode("p", "This is a paragraph", None, None)
        node2 = HTMLNode("p", "This is a paragraph", None, None)
        self.assertEqual(node, node2)

        node_props = {

            "href": "https://www.google.com",
            "target": "_blank",
        }

        node = HTMLNode("a", "This is a link", None, node_props)
        node2 = HTMLNode("a", "This is a link", None, node_props)
        self.assertEqual(node, node2)

    def test_noteq(self):
        
        # Different paragraph content
        node = HTMLNode("p", "This is a paragraph")
        node2 = HTMLNode("p", "This is another paragraph")
        self.assertNotEqual(node, node2)

        # Different props
        node1_props = {

            "href": "https://www.bing.com",
            "target": "_blank",

        }
        node2_props = {

            "href": "https://www.google.com",
            "target": "_blank",

        }

        node = HTMLNode("a", "This is a link", None, node1_props)
        node2 = HTMLNode("a", "This is a link", None, node2_props)
        self.assertNotEqual(node, node2)


# Test functionality of HTML Leaf Node child class
class TestLeafNode(unittest.TestCase):

    # Create and test leaf node
    def leaf_node_create(self):

        print(Fore.GREEN + "---------------------------------------------------------------")
        print(Fore.GREEN + "Creating Leaf Node...")
        print(Fore.GREEN + "---------------------------------------------------------------")
        print(Style.RESET_ALL)

        node = LeafNode("p", "test")
        print( node.__repr__() )
    
        print("Leaf Node to HTML...")

        print( node.to_html() )

        # Create leaf node without value
        # node = LeafNode("p")

        print("Leaf Node with no tag...")

        node = LeafNode(None, "test")
        print( node.__repr__() )

        print("Leaf Node with no tag to HTML...")
        print( node.to_html() )


# Test functionality of HTML Parent Node child class
class TestParentNode(unittest.TestCase):

    # Create and test leaf node
    def parent_node_create(self):

        print(Fore.GREEN + "---------------------------------------------------------------")
        print(Fore.GREEN + "Creating Parent Node...")
        print(Fore.GREEN + "---------------------------------------------------------------")
        print(Style.RESET_ALL)

        children_list = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ]

        node = ParentNode("p", children_list)
        print( node.__repr__() )

        print("Parent Node to HTML...")
        print( node.to_html() )

        print("Parent Node with nested Parent Nodes...")
        inner_list = [
            LeafNode("b", "Bold text"),
            LeafNode("p", "inner Paragraph")
        ]
        outer_list = [
            ParentNode("p", inner_list),
            LeafNode("i", "italic text")
        ]

        node = ParentNode("p", outer_list)
        print( node.__repr__() )

        print("Nested Parent Node to HTML...")
        print( node.to_html() )

if __name__ == "__main__":
    unittest.main()