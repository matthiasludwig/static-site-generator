import os

from helper import markdown_to_html_node


def extract_title(markdown: str) -> str:
    """
    Extracts the title from a markdown string.
    The title is defined as the first line that starts with a '#' character.
    """
    lines = markdown.split('\n')
    if lines[0].strip().startswith('#'):
        heading = lines[0].strip()
        heading = heading.lstrip('#').strip()  # Remove leading '#' and whitespace
        return heading
    return ""  # Return an empty string if no title is found
    

def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str):
    # Print message
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read the markdown content from the source file
    with open(from_path, 'r') as f:
        markdown_content = f.read()

    # Read the template content from the template file
    with open(template_path, 'r') as f:
        template_content = f.read()

    html_nodes = markdown_to_html_node(markdown_content)
    html_string = "".join([node.to_html() for node in html_nodes.children])

    document_title = extract_title(markdown_content)

    # Replace the placeholder in the template with the generated HTML content
    final_html = template_content.replace("{{ Content }}", html_string)
    final_html = final_html.replace("{{ Title }}", document_title)
    # Replace links to with basepath
    final_html = final_html.replace('href="/', f'href="/{basepath}')
    final_html = final_html.replace('src="/', f'src="/{basepath}')

    # Write the final HTML content to the destination file
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    with open(os.path.join(dest_path, "index.html") , "w", encoding="utf-8") as f:
        f.write(final_html)

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str):
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        if os.path.isdir(item_path):
            generate_pages_recursive(item_path, template_path, os.path.join(dest_dir_path, item), basepath)
        else:
            if item.endswith(".md"):
                generate_page(item_path, template_path, dest_dir_path, basepath)
