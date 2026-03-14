import streamlit as st

def display_flashcards(cards):

    st.header("🧠 Flashcards")

    if not cards:
        st.info("No flashcards generated.")
        return

    # CSS for flip cards
    st.markdown("""
    <style>
    .flashcard-container {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
    }

    .flashcard {
        background-color: transparent;
        width: 250px;
        height: 160px;
        perspective: 1000px;
    }

    .flashcard-inner {
        position: relative;
        width: 100%;
        height: 100%;
        text-align: center;
        transition: transform 0.6s;
        transform-style: preserve-3d;
    }

    .flashcard:hover .flashcard-inner {
        transform: rotateY(180deg);
    }

    .flashcard-front, .flashcard-back {
        position: absolute;
        width: 100%;
        height: 100%;
        border-radius: 12px;
        padding: 15px;
        backface-visibility: hidden;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 16px;
        font-weight: 500;
    }

    .flashcard-front {
        background: #4CAF50;
        color: white;
    }

    .flashcard-back {
        background: #1E88E5;
        color: white;
        transform: rotateY(180deg);
    }
    </style>
    """, unsafe_allow_html=True)

    html = '<div class="flashcard-container">'

    for card in cards:

        front = card.get("front", "Concept")
        back = card.get("back", "Definition")

        html += f"""
        <div class="flashcard">
            <div class="flashcard-inner">
                <div class="flashcard-front">
                    {front}
                </div>
                <div class="flashcard-back">
                    {back}
                </div>
            </div>
        </div>
        """

    html += "</div>"

    st.markdown(html, unsafe_allow_html=True)