import streamlit as st
import streamlit.components.v1 as components

def display_flashcards(cards):

    if not cards:
        st.info("No flashcards generated.")
        return

    flashcard_html = """
    <style>
    .flashcard-container {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
        justify-content: center;
        padding: 20px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    .flashcard {
        background-color: transparent;
        width: 280px;
        height: 180px;
        perspective: 1000px;
        cursor: pointer;
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
        padding: 20px;
        backface-visibility: hidden;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 16px;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        border: 1px solid rgba(255,255,255,0.1);
    }

    .flashcard-front {
        background: linear-gradient(135deg, #4CAF50 0%, #388E3C 100%);
        color: white;
    }

    .flashcard-back {
        background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
        color: white;
        transform: rotateY(180deg);
    }
    </style>
    <div class="flashcard-container">
    """

    for card in cards:
        front = card.get("front", "Concept")
        back = card.get("back", "Definition")
        flashcard_html += f"""
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

    flashcard_html += "</div>"
    rows = (len(cards) // 3) + 1
    total_height = max(400, rows * 220)

    components.html(flashcard_html, height=total_height, scrolling=True)
