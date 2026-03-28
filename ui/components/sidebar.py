import streamlit as st
import os
from core.engine import process_document, create_tutor_agent
from tools.parser import text_to_md
from core.provider import get_llm
from tools.youtube_tool import get_youtube_transcript

UPLOAD_FOLDER = "uploaded_docs"

def show_sidebar():
    with st.sidebar:
        st.title("AI Tutor")

        # ----------------------------
        # Navigation Menu (NEW)
        # ----------------------------
        st.divider()
        page = st.radio(
            "Navigation",
            ["Chat", "Flashcards", "Quiz", "Analytics"]
        )

        st.session_state.page = page

        st.divider()
        input_method = st.radio("Choose Input Method", ["PDF Upload", "YouTube Link"])

        uploaded_file = None
        youtube_url = None

        if input_method == "PDF Upload":
            uploaded_file = st.file_uploader(
                "Upload Study Material (PDF)",
                type=["pdf"]
            )
        else:
            youtube_url = st.text_input("Enter YouTube Video URL")
            if st.button("Process Video"):
                pass

        # ----------------------------
        # Process Uploaded PDF
        # ----------------------------
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

        # ----------------------------
        # Process YouTube Link
        # ----------------------------
        elif youtube_url and (
            input_method == "YouTube Link"
            and "current_file" not in st.session_state
            or st.session_state.get("current_file") != youtube_url
        ):
            if input_method == "YouTube Link" and youtube_url:
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                file_path = os.path.join(UPLOAD_FOLDER, "youtube_transcript.txt")

                with st.spinner("Fetching YouTube transcript and analyzing..."):
                    try:
                        transcript = get_youtube_transcript(youtube_url)

                        if transcript.startswith("Error"):
                            st.error(transcript)

                        else:
                            with open(file_path, "w", encoding="utf-8") as f:
                                f.write(transcript)

                            llm = get_llm()
                            full_text = text_to_md(llm, file_path)
                            st.session_state.full_text = full_text

                            vector_db = process_document(file_path)
                            agent_executor = create_tutor_agent(vector_db)

                            st.session_state.vector_db = vector_db
                            st.session_state.agent_executor = agent_executor
                            st.session_state.current_file = youtube_url
                            st.session_state.messages = []
                            st.session_state.flashcards = None
                            st.session_state.quiz = None

                            st.success("Ready to study!")

                    except Exception as e:
                        st.error(f"Error: {e}")

        return uploaded_file or youtube_url