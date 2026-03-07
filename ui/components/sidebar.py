import streamlit as st
import os
from core.engine import process_document, create_tutor_agent

UPLOAD_FOLDER = "uploaded_docs"

def show_sidebar():
    with st.sidebar:
        st.title("Controls")
        
        uploaded_file = st.file_uploader(
            "Upload PDF",
            type=["pdf"]
        )

        if uploaded_file:
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)

            if "current_file" not in st.session_state or st.session_state.current_file != uploaded_file.name:
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                with st.spinner("Processing document and creating agent..."):
                    try:
                        vector_db = process_document(file_path)
                        agent_executor = create_tutor_agent(vector_db)
                        
                        st.session_state.vector_db = vector_db
                        st.session_state.agent_executor = agent_executor
                        st.session_state.current_file = uploaded_file.name
                        st.session_state.messages = [] 
                        
                        st.success("Agent is ready!")
                    except Exception as e:
                        st.error(f"Error processing document: {e}")

        return uploaded_file
