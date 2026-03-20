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

# ✅ YOUR AUDIO FEATURE IMPORT
from utils.audio_utils import generate_audio


st.set_page_config(
    page_title="Veras Notes",
    page_icon="📚",
    layout="wide"
)

st.markdown(load_css(), unsafe_allow_html=True)
show_header()

# 🔹 Sidebar
uploaded_file, menu = show_sidebar()

# 🔹 DEBUG (to confirm app is rendering)
st.write("✅ App Loaded")

# 🔹 Fix: default menu if None
if not menu:
    menu = "💬 Study Chat"

# Session state
if "flashcards" not in st.session_state:
    st.session_state.flashcards = None
if "quiz" not in st.session_state:
    st.session_state.quiz = None


# ================== MAIN LOGIC ==================

# 🔥 TEMP FIX: run even without file
if True:

    # 🔹 Dummy response if no file uploaded
    if uploaded_file:
        response = chat_interface()
    else:
        st.warning("No file uploaded. Showing demo content.")
        response = """Artificial Intelligence (AI) is the simulation of human intelligence in machines.
        It enables systems to learn from data, make decisions, and improve over time.
        AI is widely used in applications like chatbots, recommendation systems, and self-driving cars."""

    # ---------- 💬 STUDY CHAT ----------
    if menu == "💬 Study Chat":
        st.subheader("💬 Study Companion")

        if response:
            st.subheader("📄 Summary")
            st.write(response)

            # 🎧 YOUR AUDIO FEATURE
            if st.button("🎧 Generate Audio Summary"):
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

    # ---------- 🧠 FLASHCARDS ----------
    elif menu == "🧠 Flashcards":
        st.subheader("🧠 Knowledge Flashcards")

        if st.button("Generate Flashcards from Document"):
            with st.spinner("Creating flashcards..."):
                st.session_state.flashcards = generate_flashcards(response)

        if st.session_state.flashcards:
            display_flashcards(st.session_state.flashcards)
        else:
            st.info("Click the button to generate flashcards.")

    # ---------- 📝 QUIZ ----------
    elif menu == "📝 Quiz":
        st.subheader("📝 Practice Quiz")

        if st.button("Generate Quiz from Document"):
            with st.spinner("Creating quiz..."):
                st.session_state.quiz = generate_quiz(response)

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

                for i, q in enumerate(st.session_state.quiz):
                    if st.session_state.user_answers.get(i) == q.get("answer"):
                        score += 1

                st.success(f"🎯 Your Score: {score} / {len(st.session_state.quiz)}")

                with st.expander("Show Correct Answers"):
                    for i, q in enumerate(st.session_state.quiz):
                        st.write(
                            f"**Q{i+1}:** {q.get('question')} | **Correct: {q.get('answer')}**"
                        )

        else:
            st.info("Click the button to generate quiz.")