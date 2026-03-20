import json
from core.provider import get_llm
from tools.parser import extract_json_from_text

def generate_flashcards(text: str, num_cards: int = 10):
    """
    Generates flashcards from educational text.
    """

    llm = get_llm()

    prompt = f"""
You are an AI that creates study flashcards.

IMPORTANT RULES:
- Return ONLY valid JSON array
- Do NOT include explanations, tables, or markdown formatting
- Output must start with [ and end with ]

Format:

[
  {{
    "front": "question or concept",
    "back": "definition or explanation"
  }}
]

Generate {num_cards} flashcards from the text below.

TEXT:
{text}
"""

    response = llm.invoke(prompt)

    try:
        content = response.content
        return extract_json_from_text(content)
    except Exception as e:
        print(f"Error generating flashcards: {e}")
        return []
