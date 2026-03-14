'''import streamlit as st
import sys
import os

# Add the project root to the python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from ui.components.header import show_header
from ui.components.sidebar import show_sidebar
from ui.components.chat import chat_interface
from ui.styles.css import load_css


st.set_page_config(
    page_title="Educational AI Agent",
    page_icon="📚",
    layout="wide"
)

st.markdown(load_css(), unsafe_allow_html=True)

show_header()

uploaded_file = show_sidebar()

if uploaded_file:
    st.success("PDF uploaded successfully!")

chat_interface()'''

import streamlit as st
import sys
import os
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)
from ui.components.header import show_header
from ui.components.sidebar import show_sidebar
from ui.components.chat import chat_interface
from ui.styles.css import load_css
from tools.flashcard_tool import generate_flashcards
from tools.quiz_tool import generate_quiz
from ui.flashcard_ui import display_flashcards

st.set_page_config(
    page_title="Educational AI Agent",
    page_icon="📚",
    layout="wide"
)
st.markdown(load_css(), unsafe_allow_html=True)
show_header()
uploaded_file = show_sidebar()

if uploaded_file:

    
    upload_folder = "uploaded_docs"
    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("PDF uploaded successfully!")

    
    response = chat_interface()

    
    if response:

        st.divider()

        
        st.subheader("Flashcards")

        flashcards = generate_flashcards(response)

        if flashcards:
            display_flashcards(flashcards)
        else:
            st.info("No flashcards generated.")

        st.divider()

        
        st.subheader("📝Quiz")

        quiz = generate_quiz(response)

        if quiz:
            for i, q in enumerate(quiz):

                st.write(f"**Q{i+1}: {q.get('question')}**")

                if q.get("type") == "mcq":
                    for option in q.get("options", []):
                        st.write("-", option)

                if st.button(f"Show Answer {i+1}"):
                    st.success(f"Answer: {q.get('answer')}")

        else:
            st.info("No quiz generated.")