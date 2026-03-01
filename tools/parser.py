import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(script_dir))

from core.provider import get_llm
from markitdown import MarkItDown

def text_to_md(client, source: str) -> str:
    """
    Converts a document to Markdown. 
    If an image is found, it uses the groq client to describe it.
    """

    if not source.startswith("http") and not os.path.exists(source):
        raise FileNotFoundError(f"The file/video at {source} was not found.")

    try:
        md = MarkItDown(llm_client=client, llm_model="llama-3.2-11b-vision-preview")
        result = md.convert(source)
        return result.text_content

    except Exception as e:
        return str(e)
