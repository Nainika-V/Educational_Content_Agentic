import config
from langchain_groq import ChatGroq
def get_llm():
    """
    Returns a ChatGroq object
    """
    return ChatGroq(
        model=config.MODEL_NAME,
        temperature=config.TEMPERATURE,
        max_retries=config.MAX_RETRIES,
        api_key=config.GROQ_API_KEY
    )
