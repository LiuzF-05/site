from src.textnode import TextNode, TextType
import re

#function to split text into sub texts based on delimiters such as ** and _
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes=[]
    delimiter_list=["**","`","_", None]
    if delimiter not in delimiter_list:
        raise ValueError(f"invalid delimiter: {delimiter}")
    for node in old_nodes:
        if node.text_type!=TextType.TEXT:
            new_nodes.append(node)
        elif delimiter==None:
            new_nodes.append(TextNode(node.text, TextType.TEXT))
        else:
            parts=node.text.split(delimiter)
            if len(parts)%2==0:
                raise Exception("unmatched delimiter")
            for idx, part in enumerate(parts):
                current_text_type=text_type
                if idx%2==0:
                    current_text_type=TextType.TEXT
                if part!="":
                    new_nodes.append(TextNode(part, current_text_type))
    return new_nodes

#function to split images into sub texts that are converted into leafnodes

def split_nodes_images(old_nodes):
    new_nodes=[]
    #iterates over each node
    for node in old_nodes:
        #validates if the node's type is text (not bold, italic, etc.)
        if node.text_type!=TextType.TEXT:
            new_nodes.append(node)
            continue
        current_text=node.text
        images=extract_markdown_images(current_text)
        #appends the text if there are no images
        if not images:
            new_nodes.append(node)
            continue
        #loops until images is empty
        while images:
            image_alt, image_url=images[0]
            parts=current_text.split(f"![{image_alt}]({image_url})", 1)
            #validates if text is present and resets the loop if it isn't
            if image_alt == "":
                if parts[0] != "":
                    new_nodes.append(TextNode(parts[0], TextType.TEXT))
                current_text = parts[1]
                images = extract_markdown_images(current_text)
                continue
            #checks if the string isn't empty 
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            #creates link node, changes text to be iterated over and restarts loop
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
            current_text=parts[1]
            images=extract_markdown_images(current_text)
        #adds any leftover text from loop
        if current_text!="":
            new_nodes.append(TextNode(current_text, TextType.TEXT))
        
    return new_nodes

#function to split links into sub texts that are converted into leafnodes

def split_nodes_links(old_nodes):
    new_nodes=[]
    #iterates over each node
    for node in old_nodes:
        #validates if the node's type is text (not bold, italic, etc.)
        if node.text_type!=TextType.TEXT:
            new_nodes.append(node)
            continue
        current_text=node.text
        links=extract_markdown_links(current_text)
        #appends the text if there are no links
        if not links:
            new_nodes.append(node)
            continue
        #loops until links is empty
        while links:
            link_anchor, link_url=links[0]
            parts=current_text.split(f"[{link_anchor}]({link_url})", 1)
            #validates if text is present and resets the loop if it isn't
            if link_anchor == "":
                if parts[0]:
                    new_nodes.append(TextNode(parts[0], TextType.TEXT))
                current_text = parts[1]
                links = extract_markdown_links(current_text)
                continue         
            #checks if the string isn't empty   
            if parts[0]!="":
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            #creates link node, changes text to be iterated over and restarts loop
            new_nodes.append(TextNode(link_anchor, TextType.LINK, link_url))
            current_text=parts[1]
            links=extract_markdown_links(current_text)
        #adds any leftover text from loop
        if current_text!="":
            new_nodes.append(TextNode(current_text, TextType.TEXT))
        
    return new_nodes

#function to extract the url and alt text of an image from a markdown text
def extract_markdown_images(text):
    tuples= re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return tuples

#function to extract the url and anchor text of a link from a markdown text
def extract_markdown_links(text):
    tuples= re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return tuples

def extract_title(md):
    lines=md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[1:].strip()
    raise Exception("no h1 header found")