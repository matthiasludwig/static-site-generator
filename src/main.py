from textnode import TextNode, TextType
import os, shutil

'''
Recursive function to copy static files from the static directory to the public directory
First ensures that the public directory is empty and deletes any files in it.
'''
def copy_static(source: str, dest: str):
    # First check if the destination directory exists
    if not os.path.exists(dest):
        os.mkdir(dest)
    for filename in os.listdir(source):
        file_path = os.path.join(source, filename)
        dest_path = os.path.join(dest, filename)
        print(f"Copying {file_path} to {dest_path}")
        if os.path.isfile(file_path):
            shutil.copy(file_path, dest_path)
        elif os.path.isdir(file_path):
            copy_static(file_path, dest_path)


'''
Cleanup function for the public directory. Deletes all files and directories in the public directory.
'''

def clean_up(dest: str):
    if os.path.exists(dest) and os.path.isdir(dest):
        print(f"Cleaning up {dest}")
        shutil.rmtree(dest)
        os.mkdir(dest)


def main():
    clean_up("public")
    copy_static("static", "public")

main()