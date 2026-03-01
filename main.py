from core.provider import get_llm
from tools.parser import text_to_md
from prompts.system_prompt import TUTOR_SYSTEM_PROMPT, SUMMARIZATION_INSTRUCTIONS

def start_study_session(file_path):
    llm = get_llm()
    raw_markdown = text_to_md(llm, file_path)

    messages = [ ("system", TUTOR_SYSTEM_PROMPT),("human", f"{SUMMARIZATION_INSTRUCTIONS}\n\nDOCUMENT START:\n{raw_markdown}\nDOCUMENT END")]

    response = llm.invoke(messages)
    
    return response.content

if __name__ == "__main__":
    output = start_study_session("how to install and where.txt")
    print("\n" + "="*20 + " TUTOR OUTPUT " + "="*20 + "\n")
    print(output)