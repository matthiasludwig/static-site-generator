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
    

