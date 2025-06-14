from src.textnode import TextNode, TextType
from src.htmlnode import LeafNode, ParentNode
from src.splitter import *
from src.blocktype import BlockType
import re

#function to convert text into textnode with it's respective type
def text_to_textnode(text):
    final=[TextNode(text, TextType.TEXT)]
    final=split_nodes_delimiter(final, "**", TextType.BOLD)
    final=split_nodes_delimiter(final, "_", TextType.ITALIC)
    final=split_nodes_delimiter(final, "`", TextType.CODE)
    final=split_nodes_images(final)
    final=split_nodes_links(final)
    return final

#function to convert textnodes to htmlnodes by adding tags and props
def textnode_to_htmlnode(text_node):
    match (text_node.text_type):
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)

        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)

        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)

        case TextType.LINK:
            if not text_node.url:
                raise ValueError("link text type requires a url")
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        
        case TextType.IMAGE:
            if not text_node.url:
                raise ValueError("image text type requires a url")
            return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
        
        case _:
            raise ValueError("invalid text_type")

#function to split markdown text into blocks
def markdown_to_blocks(markdown):
    blocks=markdown.split("\n\n")
    filtered=[]
    for block in blocks:
        if block.strip()=="":
            continue
        filtered.append(block.strip())
    return filtered

#function to convert the blocks into blocktypes
def block_to_blocktype(block):
    lines=block.split("\n")

    if not block:
        raise ValueError("empty block")
    
    if len(lines)>1 and lines[0].strip().startswith("```") and lines[-1].strip().startswith("```"):
        return BlockType.CODE   
    
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
 
    if block.startswith("1. "):
        i=1
        for line in lines:
            if not line.strip().startswith(f"{i}. "):
                break
            i+=1
        else:
            return BlockType.ORDERED_LIST
    
    if block.startswith("> "):
        for line in lines:
            if not line.startswith("> "):
                break
        else:
            return BlockType.QUOTE
    
    if block.startswith("- "):
        for line in lines:  
            if not line.strip().startswith("- "):
                break
        else:
            return BlockType.UNORDERED_LIST  
     
    return BlockType.PARAGRAPH

def text_to_children(text):
    return list(map(lambda node: textnode_to_htmlnode(node), text_to_textnode(text)))

def block_to_htmlnode(block):
    children=[]
    block_type=block_to_blocktype(block)
    match (block_type):
        case BlockType.QUOTE:
           text=[]
           for line in block.split("\n"):
               text.append(line[2:])               
           children.append(ParentNode(tag="blockquote", children=text_to_children("\n".join(text))))
        
        case BlockType.UNORDERED_LIST:
            ulist=[]
            for line in block.split("\n"):
                if line.startswith("- "):
                    ulist.append(ParentNode(tag="li", children=text_to_children(line.strip()[2:])))
            children.append(ParentNode(tag="ul", children=ulist))
        
        case BlockType.ORDERED_LIST:
            olist=[]
            for line in block.split("\n"):
                olist.append(ParentNode(tag="li", children=text_to_children(line.strip()[3:])))
            children.append(ParentNode(tag="ol", children=olist))
        
        case BlockType.CODE:
            text=block[block.find("```")+4:block.rfind("```")]
            children.append(ParentNode(tag="pre", children=[LeafNode(tag="code", value=text)]))

        case BlockType.PARAGRAPH:
            children.append(ParentNode(tag="p", children=text_to_children(" ".join(block.split("\n")))))

        case BlockType.HEADING:
            head=0
            for char in block:
                if char=="#":
                    head+=1
                else:
                    break
            children.append(ParentNode(tag=f"h{head}", children=text_to_children(block[head+1:])))
    return children
        

def markdown_to_htmlnode(markdown):
    blocks=markdown_to_blocks(markdown)
    final=[]
    for block in blocks:
        final.extend(block_to_htmlnode(block))
        
    return ParentNode(tag="div", children=final)


    
