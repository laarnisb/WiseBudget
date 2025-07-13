import bleach
import html

def sanitize_input(text: str) -> str:
    """
    Clean user input by removing potentially dangerous HTML or JavaScript content.
    """
    if not isinstance(text, str):
        return ""
    return bleach.clean(text, tags=[], attributes={}, strip=True)

def escape_output(text: str) -> str:
    """
    Escape special characters (e.g., <, >) before displaying to prevent XSS.
    """
    if not isinstance(text, str):
        return ""
    return html.escape(text)
