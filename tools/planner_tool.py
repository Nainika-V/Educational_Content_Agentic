from core.provider import get_llm

def generate_study_plan(content: str, doc_name: str):
    """
    Analyzes the content and generates a proactive 3-day study plan.
    """
    llm = get_llm()

    prompt = f"""
You are an expert Learning Architect. You have just been given a document titled '{doc_name}'.

Based on the content provided below, create a proactive '3-Day Mastery Plan' for a student.

Your plan should:
1. **Analyze Complexity:** Briefly state how difficult this material is.
2. **Day 1 (Foundations):** What core concepts should they focus on first?
3. **Day 2 (Deep Dive):** What are the trickier parts they should study next?
4. **Day 3 (Assessment):** What should they be able to explain or solve by the end?

CONTENT SUMMARY/TEXT:
{content[:5000]}  # Using first 5000 chars for context

Format the response in beautiful Markdown with emojis.
"""

    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"Could not generate a study plan: {e}"
