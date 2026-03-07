from langchain.agents import create_agent
from core.provider import get_llm
from tools.parser import text_to_md
from tools.chunker import chunk_text
from core.vector_store import store_chunks
from tools.retrieval_tool import create_retrieval_tool
from prompts.system_prompt import TUTOR_SYSTEM_PROMPT

def process_document(file_path):
    """
    Processes a document: converts to MD, chunks, and stores in ChromaDB.
    Returns the vector database.
    """
    llm = get_llm()
    raw_markdown = text_to_md(llm, file_path)
    chunks = chunk_text(raw_markdown)
    vector_db = store_chunks(chunks)
    return vector_db

def create_tutor_agent(vector_db):
    """
    Creates a LangChain agent with retrieval tools using the agent.
    """
    llm = get_llm()
    retrieval_tool = create_retrieval_tool(vector_db)
    tools = [retrieval_tool]
    
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
        messages.append({"role": role, "content": content})
    
    messages.append({"role": "user", "content": query})
    result = agent.invoke({"messages": messages})
    
    if isinstance(result, dict) and "messages" in result:
        return result["messages"][-1].content
    elif hasattr(result, "content"):
        return result.content
    else:
        return str(result)
