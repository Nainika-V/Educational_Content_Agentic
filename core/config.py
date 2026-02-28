from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import getpass

load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
MODEL_NAME = 'openai/gpt-oss-20b'
TEMPERATURE = 0.3
MAX_RETRIES = 2

if "GROQ_API_KEY" not in os.environ:
    os.environ["GROQ_API_KEY"] = getpass.getpass("Enter your Groq API key: ")


