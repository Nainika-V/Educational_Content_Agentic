import streamlit as st
import sys
import os

# Add project root to Python path
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

# ✅ YOUR IMPORT
from utils.audio_utils import generate_audio


st.set_page_config(
    page_title="Educational AI Agent",
    page_icon="📚",
    layout="wide"
)

# Load CSS
st.markdown(load_css(), unsafe_allow_html=True)

# Header
show_header()

# Sidebar (file upload)
uploaded_file = show_sidebar()

# Store results in session
if "flashcards" not in st.session_state:
    st.session_state.flashcards = None

if "quiz" not in st.session_state:
    st.session_state.quiz = None


# ================== ✅ MAIN LOGIC ==================

# 👉 If file uploaded → use real flow
if uploaded_file:

    upload_folder = "uploaded_docs"
    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("PDF uploaded successfully!")

    response = chat_interface()

# 👉 If NO file → use dummy text (for testing your part)
else:
    st.warning("No file uploaded. Showing demo content.")
    response = """Artificial Intelligence (AI) is the simulation of human intelligence in machines.
    It enables systems to learn from data, make decisions, and improve over time.
    AI is widely used in applications like chatbots, recommendation systems, and self-driving cars."""


# ================== COMMON DISPLAY ==================
if response:

    # ---------------- SUMMARY ----------------
    st.subheader("📄 Summary")
    st.write(response)

    # 🎧 AUDIO FEATURE (YOUR PART)
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

    st.divider()

    # ---------------- FLASHCARDS ----------------
    st.subheader("🧠 Flashcards")

    if st.button("Generate Flashcards"):
        st.session_state.flashcards = generate_flashcards(response)

    if st.session_state.flashcards:
        display_flashcards(st.session_state.flashcards)
    else:
        st.info("Click the button to generate flashcards.")

    st.divider()

    # ---------------- QUIZ ----------------
    st.subheader("📝 Quiz")

    if st.button("Generate Quiz"):
        st.session_state.quiz = generate_quiz(response)

    if st.session_state.quiz:

        user_answers = []

        for i, q in enumerate(st.session_state.quiz):

            st.write(f"**Q{i+1}: {q.get('question')}**")

            if q.get("type") == "mcq":

                ans = st.radio(
                    "Choose an answer",
                    q.get("options", []),
                    key=f"quiz_{i}"
                )

            elif q.get("type") == "true_false":

                ans = st.radio(
                    "Choose",
                    ["True", "False"],
                    key=f"quiz_{i}"
                )

            user_answers.append(ans)

        if st.button("Submit Quiz"):

            score = 0

            for i, q in enumerate(st.session_state.quiz):
                if user_answers[i] == q.get("answer"):
                    score += 1

            st.success(f"🎯 Your Score: {score} / {len(st.session_state.quiz)}")

    else:
        st.info("Click the button to generate quiz.")