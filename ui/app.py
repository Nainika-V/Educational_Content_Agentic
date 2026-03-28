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
from utils.audio_utils import generate_audio
from tools.adaptive_tool import generate_remedial_guide


st.set_page_config(
    page_title="Veras Notes",
    page_icon="📚",
    layout="wide"
)

st.markdown(load_css(), unsafe_allow_html=True)
show_header()
document_source = show_sidebar()
st.write("App Loaded")

if "flashcards" not in st.session_state:
    st.session_state.flashcards = None
if "quiz" not in st.session_state:
    st.session_state.quiz = None
if "remedial_guide" not in st.session_state:
    st.session_state.remedial_guide = None
if "missed_questions" not in st.session_state:
    st.session_state.missed_questions = []


# ================== MAIN LOGIC ==================

# TEMP FIX: run even without file
if True:

    #Dummy response if no file uploaded
    if document_source:
        response = chat_interface()
    else:
        st.warning("No file uploaded. Showing demo content.")
        response = """Artificial Intelligence (AI) is the simulation of human intelligence in machines.
        It enables systems to learn from data, make decisions, and improve over time.
        AI is widely used in applications like chatbots, recommendation systems, and self-driving cars."""

    tab1, tab2, tab3 = st.tabs(["Study Chat", "Flashcards", "Quiz"])

    # ---------- STUDY CHAT ----------
    with tab1:
        st.subheader("Study Companion")

        if response:
            st.subheader("Summary")
            st.write(response)
            if st.button("Generate Audio Summary"):
                with st.spinner("Generating audio..."):
                    audio_path = generate_audio(response)

                    audio_bytes = open(audio_path, "rb").read()

                    st.success("Audio generated!")
                    st.audio(audio_bytes, format="audio/mp3")

                    st.download_button(
                        label="⬇ Download Audio",
                        data=audio_bytes,
                        file_name="summary.mp3",
                        mime="audio/mp3"
                    )

    # ---------- FLASHCARDS ----------
    with tab2:
        # subheader and grid is now handled in display_flashcards
        if st.button("Generate Flashcards from Document"):
            with st.spinner("Creating flashcards..."):
                st.session_state.flashcards = generate_flashcards(response)

        if st.session_state.flashcards:
            display_flashcards(st.session_state.flashcards)
        else:
            st.info("Click the button to generate flashcards.")

    # ---------- QUIZ ----------
    with tab3:
        st.subheader("Practice Quiz")

        if st.button("Generate New Quiz"):
            with st.spinner("Creating quiz..."):
                st.session_state.quiz = generate_quiz(response)
                st.session_state.remedial_guide = None
                st.session_state.missed_questions = []

                if "user_answers" in st.session_state:
                    del st.session_state.user_answers

        if st.session_state.quiz:

            if "user_answers" not in st.session_state:
                st.session_state.user_answers = {}

            for i, q in enumerate(st.session_state.quiz):
                st.write(f"**Q{i+1}: {q.get('question')}**")

                if q.get("type") == "mcq":
                    st.session_state.user_answers[i] = st.radio(
                        "Select Answer",
                        q.get("options", []),
                        key=f"quiz_{i}"
                    )

                elif q.get("type") == "true_false":
                    st.session_state.user_answers[i] = st.radio(
                        "Answer",
                        ["True", "False"],
                        key=f"quiz_{i}"
                    )

            if st.button("Submit My Quiz"):
                score = 0
                st.session_state.missed_questions = []

                for i, q in enumerate(st.session_state.quiz):
                    user_ans = st.session_state.user_answers.get(i)
                    correct_ans = q.get("answer")
                    
                    if user_ans == correct_ans:
                        score += 1
                    else:
                        st.session_state.missed_questions.append({
                            "question": q.get("question"),
                            "answer": correct_ans,
                            "user_answer": user_ans
                        })

                st.success(f"Your Score: {score} / {len(st.session_state.quiz)}")

                if st.session_state.missed_questions:
                    st.warning(f"You missed {len(st.session_state.missed_questions)} questions.")
                else:
                    st.balloons()
                    st.success("Perfect Score!")

                with st.expander("Show Correct Answers"):
                    for i, q in enumerate(st.session_state.quiz):
                        st.write(
                            f"**Q{i+1}:** {q.get('question')} | **Correct: {q.get('answer')}**"
                        )

            # Remedial Guide Section
            if st.session_state.missed_questions:
                st.divider()
                st.subheader("Personalized Remedial Guide")
                st.info("Based on your missed questions, I can generate a custom study guide to help you master these concepts.")
                
                if st.button("Generate Remedial Guide"):
                    with st.spinner("Analyzing your results and creating a guide..."):
                        st.session_state.remedial_guide = generate_remedial_guide(
                            st.session_state.missed_questions,
                            response
                        )

            if st.session_state.remedial_guide:
                st.markdown(st.session_state.remedial_guide)
                
                if st.button("Download Remedial Guide (Text)"):
                    st.download_button(
                        label="⬇ Download Study Guide",
                        data=st.session_state.remedial_guide,
                        file_name="remedial_study_guide.md",
                        mime="text/markdown"
                    )

        else:
            st.info("Click the button to generate quiz.")