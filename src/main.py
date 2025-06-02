from textnode import TextType, TextNode
from htmlnode import *
from markdown_blocks import *

import re
import os
import shutil

### Functions ###

# clear public directory
def ClearPublic(root):

    directory_list = os.listdir(root)

    for entry in directory_list:

        # build full path to each entry
        entry_path = os.path.join(root, entry)

        if(os.path.isfile(entry_path)):
            os.remove(entry_path)
        else:
            ClearPublic(entry_path)
            os.rmdir(entry_path)

# copy static directory to public
def CopyToPublic(root):
    
    # list files/folders in directory
    directory_list = os.listdir(root)

    for entry in directory_list:

        # build full path to entry from root
        entry_path = os.path.join(root, entry)

        # if file
        if(os.path.isfile(entry_path)):
            
            # replace static path with public path
            dest_path = entry_path.replace("./static", "./public")

            # copy static path to public path
            shutil.copy(entry_path, dest_path)
            
        # if folder
        else:
            
            # replace static path with public path
            dest_path = entry_path.replace("./static", "./public")

            # create folder in public path
            os.mkdir(dest_path)

            # Copy files in folder
            CopyToPublic(entry_path)

# Extract title from markdown, markdown document should begin with single header line with title
# if no title, raise exception
def extract_title(markdown):

    # Pattern for 1 '#' preceded by a space
    pattern = r'^#{1} '

    # If title line matches specified pattern
    if re.match(pattern, markdown):

        # return title line string without # and preceding space as well as new line char at end
        markdown = markdown.split('# ')[1]
        return markdown[0:-1]

    else:
        raise Exception("Invalid Title Line in Markdown, please begin markdown file with h1 header title")

# generate html page from markdown file
def generate_page(from_path, template_path, dest_path):

    print("-----------------------------------------------------")
    print(f"Generating page from {from_path} to {dest_path}...")
    print("-----------------------------------------------------")

    # validate existence of markdown file
    if os.path.exists(from_path):
        
        # open markdown file and extract title into string
        with open(from_path, 'r', encoding="utf-8") as md_file:

            # extract first line of markdown file
            titleLine = md_file.readline()

            # Attempt to extract title from markdown
            pageTitle = extract_title(titleLine)

            print("-----------------------------------------------------")
            print("Page Title successfully extracted")
            print(f"Page Title is: {pageTitle}")
            print("-----------------------------------------------------")

        # re-open markdown file to extract full markdown into string
        with open(from_path, 'r', encoding="utf-8") as md_file:

            # extract markdown string
            markdown_string = md_file.read()
    else:
        raise Exception("Markdown index.md file does not exist! Please place on in content directory")

    # check for existence of template file
    if os.path.exists(template_path):

        # open template file and extract template HTML into string variable
        with open(template_path, 'r', encoding="utf-8") as template_file:
            
            # extract template html string
            template_string = template_file.read()

    # convert markdown to html string
    md_html = markdown_to_html_node(markdown_string).to_html()

    # replace {{ Title }} in template with page title
    full_html_string = template_string.replace("{{ Title }}", pageTitle)

    # replace {{ Content }} in template with md_html string
    full_html_string = full_html_string.replace("{{ Content }}", md_html)

    # create destination file and write full html string to it
    with open(dest_path, 'w') as dest_file:

        dest_file.write(full_html_string)

    return 

# find all markdown files and generate html pages recursively
def generate_pages_recursive(from_path, template_path, dest_path):
    return

    
# Main
def main():

    # clear public directory and copy static directory to public
    ClearPublic("./public")
    CopyToPublic("./static")

    # look for index.md in content directory
    markdown_dir = "./content/index.md"

    # set destination directory
    dest_path = "./public/index.html"

    # set template html path
    template_path = "./template.html"

    generate_page(markdown_dir, template_path, dest_path)

    print("Page successfully generated")

    # debugging my god
    test_dir = "./content/index_test.md"

    with open(test_dir, 'r') as md_file:
        md_string = md_file.read()

    return

main()