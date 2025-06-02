from textnode import *
from htmlnode import *

import re


# split list of text nodes into new text nodes of correct type based on delimiter
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    
    new_nodes = []

    # Iterate over list of old nodes
    for node in old_nodes:

        # if text type of node is not NORMAL, add node to new list as is
        if node.text_type != TextType.NORMAL:

            new_nodes.append(TextNode(node.text, node.text_type))

        else:

            # split text value of node based on delimiter
            text_split = node.text.split(delimiter)

            # counter for parsing logic
            counter = 1

            # if length of list is an even number, indicates non-closing delimiter, raise exception
            if len(text_split) % 2 == 0:
                raise Exception("markdown line contains non-closing delimiter")

            # iterate over list of strings from split and create new text nodes based on delimiter
            for i in range(len(text_split)):

                if text_split[i] == "":
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(text_split[i], TextType.NORMAL))
                else:
                    new_nodes.append(TextNode(text_split[i], text_type))
                        
    return new_nodes

# split list of text nodes into new text nodes of image type
def split_nodes_image(old_nodes):

    new_nodes = []

    for node in old_nodes:

        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        
        # keep track of original text
        original_text = node.text

        # extract image markdown from node's text
        images = extract_markdown_images(original_text)

        # if no images in text node, add node to list
        if images == []:
            new_nodes.append(node)
        else:
            
            # iterate over images extracted from text
            for image in images:

                image_alt = image[0]
                image_link = image[1]
                sections = original_text.split(f"![{image_alt}]({image_link})", 1)

                if len(sections) != 2:
                    raise ValueError("invalid markdown, image section not closed")

                if sections[0] != "":
                    new_nodes.append(TextNode(sections[0], TextType.NORMAL))

                new_nodes.append(
                    TextNode(
                        image_alt,
                        TextType.IMG,
                        image_link
                    )
                )

                original_text = sections[1]
            
            if original_text != "":
                new_nodes.append(TextNode(original_text, TextType.NORMAL))

    return new_nodes

# split list of text nodes into new text nodes of link type
def split_nodes_link(old_nodes):

    new_nodes = []

    for node in old_nodes:

        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        
        # keep track of original text node text
        original_text = node.text 

        # extract link markdown from node's text
        links = extract_markdown_links(original_text)

        # if no links in text node, add node to list
        if links == []:
            new_nodes.append(node)
        else:

            # iterate over links extracted from text
            for link in links:

                link_text = link[0]
                link_target = link[1]
                sections = original_text.split(f"[{link_text}]({link_target})", 1)

                if len(sections) != 2:
                    raise ValueError("invalid markdown, image section not closed")

                if sections[0] != "":
                    new_nodes.append(TextNode(sections[0], TextType.NORMAL))

                new_nodes.append(
                    TextNode(
                        link_text,
                        TextType.LINK,
                        link_target
                    )
                )

                original_text = sections[1]
            
            if original_text != "":
                new_nodes.append(TextNode(original_text, TextType.NORMAL))

                ''' 
                # My old working method of dynamically extracting links ( works for images too )

                # check if first index has links in it ( not first link ), and if it does, remove all but trailing text
                if extract_markdown_links(sections[0]) != []:
                    trailing_text = sections[0][sections[0].rfind(")") + 1 :]
                    new_nodes.append(TextNode(trailing_text, TextType.NORMAL))
                    new_nodes.append(TextNode(link_text, TextType.LINK, link_target))
                else:
                    new_nodes.append(TextNode(sections[0], TextType.NORMAL))
                    new_nodes.append(TextNode(link_text, TextType.LINK, link_target))
                '''

    return new_nodes

# extract image information from markdown
def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

# extract link information from markdown
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

# Parse 1 main text block into individual text nodes
def text_to_textnodes(text):

    nodes = [TextNode(text, TextType.NORMAL)]

    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)

    return nodes