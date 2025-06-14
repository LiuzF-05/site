from src.textnode import TextType, TextNode
from src.htmlnode import HTMLNode, LeafNode, ParentNode
from src.converter import *
from src.splitter import *
from src.site_generating import copy_to_public, generate_page, generate_pages_recursive
import sys

def main():
  basepath="/"
  if len(sys.argv)>1:
    basepath=sys.argv[1]
  print(basepath)
  copy_to_public("./static","./docs")
  generate_pages_recursive("./content","./template.html", "./docs", basepath)
main()