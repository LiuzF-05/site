from enum import Enum

#all possible texttypes
class TextType(Enum):
    TEXT=1
    BOLD=2
    ITALIC=3
    CODE=4
    LINK=5
    IMAGE=6

#actual textnode code
class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text=text
        self.text_type=text_type
        self.url=url

#compare two texttypes to eachother and returns True or False
    def __eq__(self, other):
        return self.text==other.text and self.text_type==other.text_type and self.url==other.url

#representation of the textnode
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"