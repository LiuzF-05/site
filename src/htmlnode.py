class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag=tag
        self.value=value
        self.children=children
        self.props=props

#method must be overriden by child class
    def to_html(self):
        raise NotImplementedError("child class must override")
    
#turns a dictionary into a string that represents the html attributes
    def props_to_html(self):
        parts=[]
        if not self.props:
            return
        for key in self.props:
            parts.append(f'{key}="{self.props[key]}"')
        final=" ".join(parts)
        return final
    
#representation of the htmlnode
    def __repr__(self):
        return f"TextNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)
    
    #turns the node into html
    def to_html(self):
        has_props=self.props_to_html()
        
        #checks if value is present
        if self.value==None:
            raise ValueError("no value passed")
        
        #checks if tag is present
        if self.tag==None:
            return self.value
        
        #checks if props is present and returns a different string if it is
        if has_props:
            return f"<{self.tag} {has_props}>{self.value}</{self.tag}>"
        return f"<{self.tag}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    #turns the node into html
    def to_html(self):
        parts=[]
        has_props=self.props_to_html()

        #checks if tag is present
        if not self.tag:
            raise ValueError("missing a tag")
        
        #checks if children is present
        if not self.children:
            raise ValueError("missing children parameter")

        #iterates through child and formats each one        
        for child in self.children:
            if not isinstance(child, HTMLNode):
                raise ValueError("child is not an HTMLNode")
            parts.append(child.to_html())

        #checks if props is present and returns a different string if it is
        if has_props:
            return f"<{self.tag} {has_props}>{"".join(parts)}</{self.tag}>"
        return f"<{self.tag}>{"".join(parts)}</{self.tag}>"