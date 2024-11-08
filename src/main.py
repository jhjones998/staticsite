from textnode import TextNode, TextType, split_nodes_delimiter
from markdown import markdown_to_html_node, extract_title

import pathlib
import os
import shutil


ROOT_DIR = (pathlib.Path(__file__) / pathlib.Path("../..")).resolve()


def main() -> None:
    copy_src_to_dest("static", "public")
    generate_pages_recursive("content", "template.html", "public")


def copy_src_to_dest(src: pathlib.Path, dest: pathlib.Path) -> None:
    src = ROOT_DIR / src
    dest = ROOT_DIR / dest
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(src, dest)


def generate_page(from_path: pathlib.Path, template_path: pathlib.Path, to_path: pathlib.Path) -> None:
    from_path = ROOT_DIR / from_path
    template_path = ROOT_DIR / template_path
    to_path = ROOT_DIR / to_path

    print(f"Generating page from {from_path} to {to_path} using template {template_path}")
    with open(from_path, "r") as f:
        markdown = f.read()
    title = extract_title(markdown)
    html_node = markdown_to_html_node(markdown)
    with open(template_path, "r") as f:
        template = f.read()
    with open(to_path, "w") as f:
        f.write(template.replace("{{ Content }}", html_node.to_html()).replace("{{ Title }}", title))


def generate_pages_recursive(dir_path_content: pathlib.Path, template_path: pathlib.Path, dir_path_public: pathlib.Path) -> None:
    dir_path_content = ROOT_DIR / dir_path_content
    template_path = ROOT_DIR / template_path
    dir_path_public = ROOT_DIR / dir_path_public
    for path in dir_path_content.iterdir():
        if path.is_dir():
            generate_pages_recursive(path, template_path, dir_path_public / path.relative_to(dir_path_content))
        elif path.suffix == ".md":
            print(path.relative_to(dir_path_content))
            if not os.path.exists(dir_path_public):
                os.makedirs(dir_path_public)
            generate_page(path, template_path, dir_path_public / path.relative_to(dir_path_content).with_suffix(".html"))


if __name__ == "__main__":
    main()
