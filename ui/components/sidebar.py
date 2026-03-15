import streamlit as st
import os
from core.engine import process_document, create_tutor_agent
from tools.parser import text_to_md
from core.provider import get_llm

UPLOAD_FOLDER = "uploaded_docs"

def show_sidebar():
    with st.sidebar:
        st.title("AI Tutor")
        
        # Navigation Menu
        menu_options = ["💬 Study Chat", "🧠 Flashcards", "📝 Quiz"]
        
        if "menu_index" not in st.session_state:
            st.session_state.menu_index = 0

        menu = st.radio(
            "Navigation",
            menu_options,
            index=st.session_state.menu_index,
            key="nav_widget"
        )
        
        st.session_state.menu_index = menu_options.index(menu)
        
        st.divider()
        
        uploaded_file = st.file_uploader(
            "Upload Study Material (PDF)",
            type=["pdf"]
        )

        if uploaded_file:
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)

            if "current_file" not in st.session_state or st.session_state.current_file != uploaded_file.name:
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                with st.spinner("Analyzing document..."):
                    try:
                        llm = get_llm()
                        full_text = text_to_md(llm, file_path)
                        st.session_state.full_text = full_text

                        vector_db = process_document(file_path)
                        agent_executor = create_tutor_agent(vector_db)
                        
                        st.session_state.vector_db = vector_db
                        st.session_state.agent_executor = agent_executor
                        st.session_state.current_file = uploaded_file.name
                        st.session_state.messages = [] 
                        st.session_state.flashcards = None
                        st.session_state.quiz = None
                        
                        st.success("Ready to study!")
                    except Exception as e:
                        st.error(f"Error: {e}")

        return uploaded_file, menu
