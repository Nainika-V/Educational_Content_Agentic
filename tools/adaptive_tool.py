from core.provider import get_llm

def generate_remedial_guide(missed_questions, context):
    """
    Generates a custom study guide based on missed quiz questions.
    """
    llm = get_llm()

    questions_str = ""
    for i, q in enumerate(missed_questions):
        questions_str += f"{i+1}. Question: {q.get('question')}\n   Correct Answer: {q.get('answer')}\n   Your Answer: {q.get('user_answer')}\n\n"

    prompt = f"""
You are an Academic Tutor helping a student who just took a quiz.
The student missed the following questions:

{questions_str}

Based on these missed questions and the provided educational context, generate a "Custom Remedial Study Guide".

Your guide should:
1. Identify the core concepts the student is struggling with.
2. Provide a clear, simplified explanation for each of those concepts.
3. Offer a "Memory Tip" or mnemonic for each concept.
4. Provide 1-2 "Deep Dive" questions for the student to think about.

EDUCATIONAL CONTEXT:
{context}

Format the response in clean Markdown.
"""

    response = llm.invoke(prompt)
    return response.content
