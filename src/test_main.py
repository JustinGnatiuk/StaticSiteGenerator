import unittest
import re
from colorama import Fore, Back, Style

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from parse import *
from markdown_blocks import *

# Testing Functionality of text_node_to_html_node
class TestTextToHTML_Leaf(unittest.TestCase):

    # Create 1 of each type of text node and convert to HTML Leaf node
    def test_text_node_to_HTML(self):

        print(Fore.GREEN + "---------------------------------------------------------------")
        print(Fore.GREEN + "Text Node to HTML Leaf Node...")
        print(Fore.GREEN + "---------------------------------------------------------------")
        print(Style.RESET_ALL)
    
        textNode = TextNode("Normal Text", TextType.NORMAL)
        print( textNode.__repr__() )
        print("LeafNode: ")
        print( text_node_to_html_node(textNode).__repr__() )
    
        textNode = TextNode("Bold Text", TextType.BOLD)
        print( textNode.__repr__() )
        print("LeafNode: ")
        print( text_node_to_html_node(textNode).__repr__() )

        textNode = TextNode("Italic Text", TextType.ITALIC)
        print( textNode.__repr__() )
        print("LeafNode: ")
        print( text_node_to_html_node(textNode).__repr__() )

        textNode = TextNode("Code Text", TextType.CODE)
        print( textNode.__repr__() )
        print("LeafNode: ")
        print( text_node_to_html_node(textNode).__repr__() )

        textNode = TextNode("Link Text", TextType.LINK)
        print( textNode.__repr__() )
        print("LeafNode: ")
        print( text_node_to_html_node(textNode).__repr__() )

        textNode = TextNode("Link Text 2", TextType.LINK, "https://boot.dev")
        print( textNode.__repr__() )
        print("LeafNode: ")
        print( text_node_to_html_node(textNode).__repr__() )

        textNode = TextNode("Image Text", TextType.IMG)
        print( textNode.__repr__() )
        print("LeafNode: ")
        print( text_node_to_html_node(textNode).__repr__() )

        textNode = TextNode("Image Text 2", TextType.IMG, "C:/ThisProgramsFolder/images/image.png")
        print( textNode.__repr__() )
        print("LeafNode: ")
        print( text_node_to_html_node(textNode).__repr__() )

    

        node = TextNode("This is a text with a `code block` word", TextType.NORMAL)
        print( node.__repr__() )
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        print(f"{new_nodes}\n")

        node = TextNode("This is a text with a **boldened** word", TextType.NORMAL)
        print( node.__repr__() )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        print(f"{new_nodes}\n")

class TestSplitNodesDelimiter(unittest.TestCase):

    # Test split_nodes_delimiter function
    def test_split_nodes_delimiter(self):
            
        print(Fore.GREEN + "---------------------------------------------------------------")
        print(Fore.GREEN + "Parse test function split_nodes_delimiter...")
        print(Fore.GREEN + "---------------------------------------------------------------")
        print(Style.RESET_ALL)

        node = TextNode("This is a text with a `code block` word", TextType.NORMAL)
        print( node.__repr__() )
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        print(f"{new_nodes}\n")

        node = TextNode("This is a text with a **boldened** word", TextType.NORMAL)
        print( node.__repr__() )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        print(f"{new_nodes}\n")

class TestTextLinkExtraction(unittest.TestCase):

    # Test extraction of links and images in text
    def test_extract_markdown_images_links(self):

        print(Fore.GREEN + "---------------------------------------------------------------")
        print(Fore.GREEN + "Parse test Extract links and images from text string...")
        print(Fore.GREEN + "---------------------------------------------------------------")
        print(Style.RESET_ALL)

        # Image extraction
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        print(text)
        print(matches)
        print()

        # Link extraction
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        print(text)
        print(matches)


class TestSplitTextNodesImage(unittest.TestCase):

    # Test the extraction of image text nodes
    def test_split_nodes_images(self):
        
        print(Fore.GREEN + "---------------------------------------------------------------")
        print(Fore.GREEN + "Parse test function split_nodes_images...")
        print(Fore.GREEN + "---------------------------------------------------------------")
        print(Style.RESET_ALL)

        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )

        new_nodes = split_nodes_image([node])

        print(new_nodes)

class TestSplitTextNodesLinks(unittest.TestCase):

    # test the extraction of link text nodes
    def test_split_nodes_links(self):
        
        print(Fore.GREEN + "---------------------------------------------------------------")
        print(Fore.GREEN + "Parse test function split_nodes_links...")
        print(Fore.GREEN + "---------------------------------------------------------------")
        print(Style.RESET_ALL)

        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [link](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )

        new_nodes = split_nodes_link([node])

        print(new_nodes)

class TestTextToTextNodes(unittest.TestCase):

    # test the extraction of markdown from text string
    def test_text_to_textnodes(self):

        print(Fore.GREEN + "---------------------------------------------------------------")
        print(Fore.GREEN + "Parse text to text nodes...")
        print(Fore.GREEN + "---------------------------------------------------------------")
        print(Style.RESET_ALL)

        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        # print the list nicely
        print(*text_to_textnodes(text), sep=",\n")

class TestMarkdownToBlocks(unittest.TestCase):

    # test the extraction of text blocks from markdown
    def test_markdown_to_blocks(self):

        print(Fore.GREEN + "---------------------------------------------------------------")
        print(Fore.GREEN + "Parse markdown into blocks...")
        print(Fore.GREEN + "---------------------------------------------------------------")
        print(Style.RESET_ALL)

        markdown = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and _italic_ words inside of it.\n\n- This is the first list item in a list block\n- This is a list item\n- This is another list item\n"

        md = """This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items"""

        blocks = markdown_to_blocks(md)
        print(blocks)
        self.assertEqual(
        blocks,
        [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ],
    )    


class TestMarkDownBlockToBlockType(unittest.TestCase):

    # test the classification of markdown block types
    def test_markdown_block_to_block_type(self):

        print(Fore.GREEN + "---------------------------------------------------------------")
        print(Fore.GREEN + "Classify markdown blocks to block types...")
        print(Fore.GREEN + "---------------------------------------------------------------")
        print(Style.RESET_ALL)

        header_block = "# This is a header"
        print(header_block)
        print(block_to_block_type(header_block))
        print()

        self.assertEqual(BlockType.HEADING, block_to_block_type(header_block))

        code_block = '``` print("Testing"); ```'
        print(code_block)
        print(block_to_block_type(code_block))
        print()

        self.assertEqual(BlockType.CODE, block_to_block_type(code_block))

        quote_block = """>This is a multi-line
>quote."""
        print(quote_block)
        print(block_to_block_type(quote_block))
        print()

        self.assertEqual(BlockType.QUOTE, block_to_block_type(quote_block))

        uList_block = "- List Item 1\n- List Item 2\n- List Item 3"
        print(uList_block)
        print(block_to_block_type(uList_block))
        print()

        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(uList_block))

        oList_block = "1. List Item 1\n2. List Item 2\n3. List Item 3"
        print(oList_block)
        print(block_to_block_type(oList_block))
        print()

        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(oList_block))

        paragraph_block = "Just a regular old paragraph with some **boldened** inline markdown"
        print(paragraph_block)
        print(block_to_block_type(paragraph_block))
        print()

        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(paragraph_block))

class TestMarkDownToHTMLParentNode(unittest.TestCase):

    # test the conversion of markdown into a parent HTML div node
    def test_markdown_to_html_parent_node(self):

        print(Fore.GREEN + "---------------------------------------------------------------")
        print(Fore.GREEN + "Convert Markdown to HTML Parent Node <div>...")
        print(Fore.GREEN + "---------------------------------------------------------------")
        print(Style.RESET_ALL)

        markdown = """This is **bolded** paragraph
text in a p
tag here

# This is a header with _italic_ text and `code` here

```
This is text that _should_ remain
the **same** even with inline stuff
```

>This is a
>multi-line quote with **bold** text

- **bold** Unordered List Item 1
- _italic_ Unordered List Item 2
- `code` Unordered List Item 3

1. **bold** Ordered List Item 1
2. _italic_ Ordered List Item 2
3. `code` Ordered List Item 3
"""

        node = markdown_to_html_node(markdown)
        html = node.to_html()
        print(html)

        #self.assertEqual(html, "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",)

if __name__ == "__main__":
    unittest.main()