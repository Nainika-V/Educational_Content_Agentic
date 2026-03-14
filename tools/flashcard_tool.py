'''import json
from core.provider import get_llm

def generate_flashcards(text: str, num_cards: int = 10):
    """
    Generates flashcards from educational text.
    Each flashcard contains a front (concept/question)
    and back (definition/explanation).
    """

    llm = get_llm()

    prompt = f"""
Extract key concepts from the text and generate {num_cards} flashcards.

Return ONLY JSON like this:

[
  {{
    "front": "concept",
    "back": "definition"
  }}
]

TEXT:
{text}
"""

    response = llm.invoke(prompt)

    try:
        return json.loads(response.content)
    except:
        return []'''
import json
from core.provider import get_llm

def generate_flashcards(text: str, num_cards: int = 10):
    """
    Generates flashcards from educational text.
    """

    llm = get_llm()

    prompt = f"""
You are an AI that creates study flashcards.

IMPORTANT RULES:
- Return ONLY valid JSON
- Do NOT include explanations
- Do NOT include tables
- Do NOT include markdown
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
        return json.loads(response.content)
    except:
        return []