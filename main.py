from core.provider import get_llm
from tools.parser import text_to_md
from prompts.system_prompt import TUTOR_SYSTEM_PROMPT, SUMMARIZATION_INSTRUCTIONS

from tools.chunker import chunk_text
from core.vector_store import store_chunks


def start_study_session(file_path):

    llm = get_llm()

    # Step 1: Convert document to markdown
    raw_markdown = text_to_md(llm, file_path)

    # Step 2: Chunk the document
    chunks = chunk_text(raw_markdown)

    # Step 3: Store in ChromaDB
    vector_db = store_chunks(chunks)

    # Week-1 summary still works
    messages = [
        ("system", TUTOR_SYSTEM_PROMPT),
        ("human", f"{SUMMARIZATION_INSTRUCTIONS}\n\nDOCUMENT START:\n{raw_markdown}\nDOCUMENT END")
    ]

    response = llm.invoke(messages)

    return response.content


if __name__ == "__main__":

    output = start_study_session("Langchain.txt")

    print("\n" + "="*20 + " TUTOR OUTPUT " + "="*20 + "\n")
    print(output)