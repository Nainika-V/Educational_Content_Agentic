import json
from core.provider import get_llm
from tools.parser import extract_json_from_text

def generate_quiz(text: str, num_questions: int = 5):
    """
    Generates quiz questions (MCQ and True/False)
    from the given educational content.
    """

    llm = get_llm()

    prompt = f"""
Create {num_questions} quiz questions from the text.

Return ONLY JSON like this:

[
  {{
    "question": "What is the capital of France?",
    "type": "mcq",
    "options": ["London", "Paris", "Berlin", "Madrid"],
    "answer": "Paris"
  }},
  {{
    "question": "Is the earth flat?",
    "type": "true_false",
    "answer": "False"
  }}
]

TEXT:
{text}
"""

    response = llm.invoke(prompt)

    try:
        content = response.content
        return extract_json_from_text(content)
    except Exception as e:
        print(f"Error generating quiz: {e}")
        return []
