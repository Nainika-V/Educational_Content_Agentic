from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def store_chunks(chunks):

    db = Chroma.from_texts(
        texts=chunks,
        embedding=embedding_model,
        persist_directory="chroma_db"
    )

    return db