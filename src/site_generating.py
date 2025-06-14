import os
import shutil
import pathlib
from src.converter import markdown_to_htmlnode
from src.splitter import extract_title

def copy_to_public(source, destination, cleaned=False):
    if not cleaned:
        if os.path.exists(destination):
            shutil.rmtree(destination)
        os.mkdir(destination)
        cleaned = True
    for file in os.listdir(source):
        file_path=os.path.join(source, file)
        if os.path.isfile(file_path):
            shutil.copy(file_path, destination)
        else:
            new_dir=os.path.join(destination, file)
            os.mkdir(new_dir)
            copy_to_public(file_path, new_dir, cleaned=False)
    return

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    if not os.path.exists(from_path):
        raise Exception("invalid origin file path")
    with open(from_path) as f:
        from_text=f.read()
    content=markdown_to_htmlnode(from_text).to_html()
    title=extract_title(from_text)
    with open(template_path) as t:
        template_text=t.read()
        template_text=template_text.replace("{{ Content }}", content).replace("{{ Title }}", title).replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    with open(dest_path, "x") as d:
        d.write(template_text)
    return 

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for file in os.listdir(dir_path_content):
        file_path=os.path.join(dir_path_content, file)
        if os.path.isfile(file_path):
            new_file=change_file_extensions(file, ".html")
            dest_file=os.path.join(dest_dir_path, new_file)
            generate_page(file_path, template_path, dest_file, basepath)
        else:
            new_dir=os.path.join(dest_dir_path, file)
            os.mkdir(new_dir)
            generate_pages_recursive(file_path, template_path, new_dir, basepath)
        
def change_file_extensions(old, extension):
    base_name=os.path.splitext(old)
    if base_name[1]==".md":
        return base_name[0]+extension
    else:
        return old