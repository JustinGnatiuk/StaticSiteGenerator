import unittest
from colorama import Fore, Back, Style

from textnode import TextNode, TextType

# Test functionality of TextNode class
class TestTextNode(unittest.TestCase):
    
    def test_text_node_create(self):

        # Create multiple types of text nodes and output them
        print(Fore.GREEN + "---------------------------------------------------------------")
        print(Fore.GREEN + "Creating Text Node...")
        print(Fore.GREEN + "---------------------------------------------------------------")
        print(Style.RESET_ALL)

        print("Node 1:")
        node = TextNode("This is a text node", TextType.BOLD)
        print( node.__repr__() )

        print("Node 2:")
        node = TextNode("This is a text node", TextType.NORMAL)
        print( node.__repr__() )

        print("Node 3:")
        node = TextNode("This is a text node", TextType.NORMAL, "https://boot.dev")
        print( node.__repr__() )

    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_noteq(self):
        
        # Different text types
        node = TextNode("This is a text node", TextType.NORMAL)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

        # Different url values
        node = TextNode("This is a text node", TextType.NORMAL, "https://boot.dev")
        node2 = TextNode("This is a text node", TextType.NORMAL)
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()