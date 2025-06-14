from src.textnode import TextType, TextNode
from src.htmlnode import HTMLNode, LeafNode, ParentNode
from src.converter import *
from src.splitter import *
from src.site_generating import copy_to_public, generate_page, generate_pages_recursive

def main():
  copy_to_public("./static","./public")
  generate_pages_recursive("./content/","./template.html", "./public/")
main()