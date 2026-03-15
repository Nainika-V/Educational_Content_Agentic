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
    page_title="Veras Notes",
    page_icon="📚",
    layout="wide"
)

st.markdown(load_css(), unsafe_allow_html=True)
show_header()
uploaded_file, menu = show_sidebar()
if "flashcards" not in st.session_state:
    st.session_state.flashcards = None
if "quiz" not in st.session_state:
    st.session_state.quiz = None
if uploaded_file:

    if menu == "💬 Study Chat":
        st.subheader("💬 Study Companion")
        chat_interface()

    elif menu == "🧠 Flashcards":
        st.subheader("🧠 Knowledge Flashcards")
        
        if st.button("Generate Flashcards from Document"):
            with st.spinner("Creating flashcards..."):
                if "full_text" in st.session_state:
                    st.session_state.flashcards = generate_flashcards(st.session_state.full_text)
                else:
                    st.error("Document content not loaded properly.")

        if st.session_state.flashcards:
            display_flashcards(st.session_state.flashcards)
        else:
            st.info("Click the button to generate flashcards from the uploaded document.")

    elif menu == "📝 Quiz":
        st.subheader("📝 Practice Quiz")
        
        if st.button("Generate Quiz from Document"):
            with st.spinner("Creating quiz..."):
                if "full_text" in st.session_state:
                    st.session_state.quiz = generate_quiz(st.session_state.full_text)
                    if "user_answers" in st.session_state:
                        del st.session_state.user_answers
                else:
                    st.error("Document content not loaded properly.")

        if st.session_state.quiz:
            if "user_answers" not in st.session_state:
                st.session_state.user_answers = {}

            for i, q in enumerate(st.session_state.quiz):
                st.write(f"**Q{i+1}: {q.get('question')}**")
                if q.get("type") == "mcq":
                    st.session_state.user_answers[i] = st.radio(
                        "Select Answer", q.get("options", []), key=f"quiz_{i}"
                    )
                elif q.get("type") == "true_false":
                    st.session_state.user_answers[i] = st.radio(
                        "Answer", ["True", "False"], key=f"quiz_{i}"
                    )

            if st.button("Submit My Quiz"):
                score = 0
                for i, q in enumerate(st.session_state.quiz):
                    if st.session_state.user_answers.get(i) == q.get("answer"):
                        score += 1
                st.success(f"🎯 Your Score: {score} / {len(st.session_state.quiz)}")
                with st.expander("Show Correct Answers"):
                    for i, q in enumerate(st.session_state.quiz):
                        st.write(f"**Q{i+1}:** {q.get('question')} | **Correct: {q.get('answer')}**")
        else:
            st.info("Click the button to generate a quiz from the uploaded document.")
else:
    st.warning("Please upload a PDF document in the sidebar to begin.")
