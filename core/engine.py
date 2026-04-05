      
from langchain.agents import create_agent
from core.provider import get_llm
from tools.parser import text_to_md
from tools.chunker import chunk_text
from core.vector_store import store_chunks
from tools.retrieval_tool import create_retrieval_tool
from prompts.system_prompt import TUTOR_SYSTEM_PROMPT
from langchain_core.tools import tool
from tools.flashcard_tool import generate_flashcards
from tools.quiz_tool import generate_quiz
import os

@tool
def flashcard_creator(topic: str):
    """
    Creates study flashcards on a topic. Searches the document context.
    """
    import streamlit as st
    from tools.retrieval_tool import search_document

    context = search_document(topic, st.session_state.vector_db) if "vector_db" in st.session_state else st.session_state.get("full_text", "")
    
    cards = generate_flashcards(context)
    st.session_state.flashcards = cards
    
    return f"I've generated {len(cards)} flashcards on '{topic}'. Please click on the 'Flashcards' tab to view them."

@tool
def quiz_creator(topic: str):
    """
    Creates a study quiz on a topic. Searches the document context.
    """
    import streamlit as st
    from tools.retrieval_tool import search_document

    context = search_document(topic, st.session_state.vector_db) if "vector_db" in st.session_state else st.session_state.get("full_text", "")
    
    quiz = generate_quiz(context)
    st.session_state.quiz = quiz

    return f"I've generated a quiz on '{topic}'. Please click on the 'Quiz' tab to view it."

def process_document(file_path):
    llm = get_llm()
    raw_markdown = text_to_md(llm, file_path)
    chunks = chunk_text(raw_markdown)
    
    # Get the filename from the path to use as a unique directory
    doc_name = os.path.basename(file_path)
    vector_db = store_chunks(chunks, doc_name)
    return vector_db


def create_tutor_agent(vector_db):
    llm = get_llm()
    
    # If vector_db is None, use a dummy retrieval tool or skip it
    if vector_db:
        retrieval_tool = create_retrieval_tool(vector_db)
        tools = [
            retrieval_tool,
            flashcard_creator,
            quiz_creator
        ]
    else:
        # Agent can still use flashcard/quiz creator based on general text
        tools = [
            flashcard_creator,
            quiz_creator
        ]
        
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=TUTOR_SYSTEM_PROMPT
    )
    return agent


def run_agent_query(agent, query, chat_history=None):
    """
    Runs a query through the agent using the messages list format.
    """
    if chat_history is None:
        chat_history = []

    messages = []

    for role, content in chat_history:
        messages.append({
            "role": role,
            "content": content
        })

    messages.append({
        "role": "user",
        "content": query
    })

    result = agent.invoke({"messages": messages})

    if isinstance(result, dict) and "messages" in result:
        return result["messages"][-1].content
    elif hasattr(result, "content"):
        return result.content
    else:
        return str(result)
