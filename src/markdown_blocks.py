import re

from enum import Enum
from htmlnode import *
from textnode import *
from parse import *


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_html_node(markdown):

    # create list of children html nodes within main div
    child_list = []

    # split markdown into blocks
    markdown_block_list = markdown_to_blocks(markdown)

    # classify each block type and convert to parent html node, then add to child list
    for block in markdown_block_list:

        match block_to_block_type(block):

            # process paragraph block type
            case BlockType.PARAGRAPH:

                # remove newline characters per standard markdown to html procedure
                block = block.replace("\n", " ")

                # determine inline children
                inline_child_list = text_to_children(block)

                # add to child node list
                child_list.append(ParentNode("p", inline_child_list, None))

            # process heading block type
            case BlockType.HEADING:
                
                # determine what header number this will be
                header_num = 0
                for character in block:

                    if character == "#":
                        header_num += 1

                    if header_num == 6:
                        continue

                # remove newline characters per standard markdown to html procedure
                block = block.replace("\n", " ")

                # remove leading pound signs that indicates header
                block = block.lstrip("#")

                # remove leading whitespace if any
                block = block.lstrip()

                # determine inline children
                inline_child_list = text_to_children(block)

                # add to child list
                child_list.append(ParentNode(f"h{header_num}", inline_child_list, None))

            # Process code block type
            case BlockType.CODE:

                # remove ` and \n characters from beginning and end of block
                #block = block.removeprefix("```\n").removesuffix("```\n")
                block = block[4:-3]

                # replace \n strings with their character literals to be maintained
                #block = block.replace("\n", "\\n")

                # create inner code node for code block [pre][code]code[/code][/pre]
                code_text = TextNode(block, TextType.CODE)
                code_node = text_node_to_html_node(code_text)

                # add to child list
                child_list.append(ParentNode("pre", [code_node], None))

            # process quote block type
            case BlockType.QUOTE:
                
                # split quote block into lines
                lines = block.split("\n")
                
                new_lines = []

                # iterate over each line and append to new line list after stripping > character and whitespace
                for line in lines:
                    new_lines.append(line.lstrip(">").strip())

                # join new line list into 1 string
                content = " ".join(new_lines)
                
                # determine inline children
                inline_child_list = text_to_children(content)

                # add to child list
                child_list.append(ParentNode("blockquote", inline_child_list, None))

            # process unordered list block type
            case BlockType.UNORDERED_LIST:
                
                # split block into lines
                line_list = block.split('\n')

                line_item_list = []

                for line in line_list:

                    # if newline character before end of markdown document adds a third empty line to unordered list block
                    if line == "":
                        break

                    # remove "- " at beginning of line
                    line = line.replace("- ", "")

                    # determine inline children
                    inline_child_list = text_to_children(line)

                    # add to line item list to build list of line items inside unordered list
                    line_item_list.append(ParentNode("li", inline_child_list, None))
                
                # add to child list
                child_list.append(ParentNode("ul", line_item_list, None))

            # process ordered list block type
            case BlockType.ORDERED_LIST:

                # split block into lines
                line_list = block.split('\n')

                line_item_list = []

                for line in line_list:

                    # if newline character before end of markdown document adds a third empty line to unordered list block
                    if line == "":
                        break
                    
                    # regex expression for a number followed by a decimal at beginning of string
                    regex_expr = r"^\d+\. "

                    # remove "[number]. " at beginning of line
                    line = re.sub(regex_expr, "", line)

                    # determine inline children
                    inline_child_list = text_to_children(line)

                    # add to line item list to build list of line items inside unordered list
                    line_item_list.append(ParentNode("li", inline_child_list, None))
                
                # add to child list
                child_list.append(ParentNode("ol", line_item_list, None))

    return ParentNode("div", child_list, None)

# build list of child html nodes from block of markdown
def text_to_children(text):

    children_list = []

    # parse text nodes out of text block
    text_nodes = text_to_textnodes(text)

    for node in text_nodes:
        children_list.append(text_node_to_html_node(node))

    return children_list

def block_to_block_type(markdown_block):

    # maybe if elif block?
    match markdown_block[0]:

        # HEADERS
        case "#":   # validate header

            # Pattern for 1-6 #'s preceded by a space
            pattern = r'^#{1,6} '

            # If the string matches the pattern
            if re.match(pattern, markdown_block):
                return BlockType.HEADING
            else:
                return BlockType.PARAGRAPH

        # CODE
        case "`": # validate code
            
            # pattern for 3 `s at the beginning of the string
            pattern1 = r'^```'

            # pattern for 3 `s at the end of the string
            pattern2 = r'```$'

            # create 2 boolean values to check for both patterns
            starts_with = bool(re.match(pattern1, markdown_block))
            ends_with = bool(re.search(pattern2, markdown_block))

            # if the string matches both patterns
            if starts_with and ends_with:
                return BlockType.CODE
            else:
                return BlockType.PARAGRAPH

        # QUOTE
        case ">": # validate quote
            
            # split quote into it's individual lines
            line_list = markdown_block.split('\n')

            # Pattern for checking for > character followed by a space
            pattern = r'^>'

            # check each line in quote
            for line in line_list:

                # if newline character before end of markdown document adds a third empty line to quote block
                if line == "":
                    break
                # return paragraph if line missing >
                if not re.match(pattern, line):
                    return BlockType.PARAGRAPH

            # return quote if all lines have >
            return BlockType.QUOTE

        # UNORDERED LIST
        case "-": # validate unordered list
            
            # split list into individual lines
            line_list = markdown_block.split('\n')

            # check each line in unordered list
            for line in line_list:

                # if newline character before end of markdown document adds a third empty line to unordered list block
                if line == "":
                    break

                # pattern to check if line begins with - followed by space
                pattern = r'^- '

                # check if each line begins with - and space, if it doesn't, block will be considered paragraph
                if re.match(pattern, line):
                    continue
                else:
                    return BlockType.PARAGRAPH

            return BlockType.UNORDERED_LIST

        # ORDERED LIST
        case "1": # validate ordered list
            
            # split ordered list into individual lines
            line_list = markdown_block.split('\n')

            # pattern to check if first line begins with "1. "
            pattern = r'^1\. '

            # Check initial line in list
            if re.match(pattern, line_list[0]) == False:
                return BlockType.PARAGRAPH

            # iterate over line list and check for sequentially numbered lines
            for i in range(1, len(line_list)):

                # dynamic regex pattern to match each line number 
                pattern = fr'^{i}\. '

                # if the line doesn't begin with "[line number]. "
                if not re.match(pattern, line_list[i-1]):
                    return BlockType.PARAGRAPH
            
            return BlockType.ORDERED_LIST

        case _: # validate paragraph
            return BlockType.PARAGRAPH


# Parse block markdown
def markdown_to_blocks(markdown):

    block_list = markdown.split('\n\n')

    for block in block_list:
        
        if block == "":
            block_list.remove(block)
        else:
            block = block.strip()

    return block_list