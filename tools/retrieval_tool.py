from langchain_core.tools import tool

def search_document(query: str, vector_db):
    """
    Searches the vector database for relevant document chunks
    """
    retriever = vector_db.as_retriever(search_kwargs={"k": 3})
    docs = retriever.invoke(query)
    results = [doc.page_content for doc in docs]
    return "\n".join(results)

def create_retrieval_tool(vector_db):
    @tool
    def document_search(query: str):
        """Search the uploaded document for relevant information and facts."""
        return search_document(query, vector_db)
    
    return document_search
