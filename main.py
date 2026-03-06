from core.provider import get_llm
from tools.parser import text_to_md
from prompts.system_prompt import TUTOR_SYSTEM_PROMPT, SUMMARIZATION_INSTRUCTIONS

from tools.chunker import chunk_text
from core.vector_store import store_chunks
from tools.retrieval_tool import search_document

def start_study_session(file_path):

    llm = get_llm()

    # Step 1: Convert document to markdown
    raw_markdown = text_to_md(llm, file_path)

    # Step 2: Chunk the document
    chunks = chunk_text(raw_markdown)

    # Step 3: Store in ChromaDB
    vector_db = store_chunks(chunks)
    '''
    # Week-1 summary still works
    messages = [
        ("system", TUTOR_SYSTEM_PROMPT),
        ("human", f"{SUMMARIZATION_INSTRUCTIONS}\n\nDOCUMENT START:\n{raw_markdown}\nDOCUMENT END")
    ]

    response = llm.invoke(messages)'''

    return vector_db 
def ask_question(query, vector_db, llm):

    context = search_document(query, vector_db)

    messages = [
        ("system", TUTOR_SYSTEM_PROMPT),
        ("human", f"Answer the question using the document context.\n\nCONTEXT:\n{context}\n\nQUESTION:\n{query}")
    ]

    response = llm.invoke(messages)

    return response.content

if __name__ == "__main__":

    vector_db = start_study_session("Nischala_reddy_curr_res.pdf")
    question = input("\nAsk a question about the document: ")

    llm = get_llm()

    answer = ask_question(question, vector_db, llm)

    print("\n" + "="*20 + " ANSWER " + "="*20 + "\n")
    print(answer)