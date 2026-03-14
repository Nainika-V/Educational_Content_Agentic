import json
from core.provider import get_llm

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
    "question": "",
    "type": "mcq",
    "options": ["A","B","C","D"],
    "answer": ""
  }},
  {{
    "question": "",
    "type": "true_false",
    "answer": "True"
  }}
]

TEXT:
{text}
"""

    response = llm.invoke(prompt)

    try:
        return json.loads(response.content)
    except:
        return []