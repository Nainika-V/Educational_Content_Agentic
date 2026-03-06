from langchain_core.tools import Tool

def search_document(query, vector_db):
    """
    Searches the vector database for relevant document chunks
    """

    retriever = vector_db.as_retriever(search_kwargs={"k": 3})

    docs = retriever.invoke(query)

    results = []

    for doc in docs:
        results.append(doc.page_content)

    return "\n".join(results)


def create_retrieval_tool(vector_db):

    retrieval_tool = Tool(
        name="Document Search",
        func=lambda query: search_document(query, vector_db),
        description="Search the uploaded document for relevant information"
    )

    return retrieval_tool