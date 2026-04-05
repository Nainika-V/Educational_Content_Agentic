import os
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def store_chunks(chunks, document_name="default"):
    # If no chunks were generated (e.g., empty file), don't crash Chroma
    if not chunks:
        print("Warning: No chunks found to store in the vector database.")
        return None

    # Create a unique directory name for this document
    clean_name = "".join(c for c in document_name if c.isalnum() or c in (" ", "_")).rstrip()
    persist_dir = os.path.join("chroma_db", clean_name.replace(" ", "_"))
    
    db = Chroma.from_texts(
        texts=chunks,
        embedding=embedding_model,
        persist_directory=persist_dir
    )

    return db