
import streamlit as st
import streamlit.components.v1 as components
import os
import random
from utils.audio_utils import generate_audio


def play_audio(text, key):
    temp_file = f"temp_card_{key}.mp3"
    try:
        audio_path = generate_audio(text, temp_file)
        with open(audio_path, "rb") as f:
            st.audio(f.read(), format='audio/mp3')

        if os.path.exists(temp_file):
            os.remove(temp_file)
    except Exception as e:
        st.error(f"Audio Error: {e}")


def get_flashcard_html(front, back, status, key):
    colors = {
        "new": "linear-gradient(135deg, #2196F3 0%, #1976D2 100%)",
        "mastered": "linear-gradient(135deg, #4CAF50 0%, #388E3C 100%)",
        "review": "linear-gradient(135deg, #f44336 0%, #d32f2f 100%)"
    }

    bg_color = colors.get(status, colors["new"])

    html = f"""
    <style>
    .flashcard-{key} {{
        background-color: transparent;
        width: 100%;
        height: 200px;
        perspective: 1000px;
        cursor: pointer;
        margin-bottom: 10px;
    }}

    .flashcard-inner-{key} {{
        position: relative;
        width: 100%;
        height: 100%;
        text-align: center;
        transition: transform 0.6s;
        transform-style: preserve-3d;
    }}

    .flashcard-{key}:hover .flashcard-inner-{key} {{
        transform: rotateY(180deg);
    }}

    .flashcard-front-{key}, .flashcard-back-{key} {{
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
        color: white;
    }}

    .flashcard-front-{key} {{
        background: {bg_color};
    }}

    .flashcard-back-{key} {{
        background: linear-gradient(135deg, #7b1fa2 0%, #4a148c 100%);
        transform: rotateY(180deg);
    }}
    </style>

    <div class="flashcard-{key}">
        <div class="flashcard-inner-{key}">
            <div class="flashcard-front-{key}">
                {front}
            </div>
            <div class="flashcard-back-{key}">
                {back}
            </div>
        </div>
    </div>
    """
    return html


def display_flashcards(cards):
    if not cards:
        st.info("No flashcards generated.")
        return

    # ✅ SESSION STATE (FIXED)
    if "card_status" not in st.session_state:
        st.session_state.card_status = {}

    for i in range(len(cards)):
        if i not in st.session_state.card_status:
            st.session_state.card_status[i] = "new"

    # Filter UI
    filter_col1, filter_col2 = st.columns([2, 1])
    with filter_col1:
        st.subheader("Knowledge Flashcards")
    with filter_col2:
        filter_status = st.selectbox(
            "Filter by Status",
            ["All", "New", "Mastered", "Need Review"],
            index=0
        )

    # Filtering
    filtered_cards = []
    for i, card in enumerate(cards):
        status = st.session_state.card_status[i]

        card_data = {
            "front": card.get("front", "Concept"),
            "back": card.get("back", "Definition"),
            "original_index": i,
            "status": status
        }

        if filter_status == "All":
            filtered_cards.append(card_data)
        elif filter_status == "New" and status == "new":
            filtered_cards.append(card_data)
        elif filter_status == "Mastered" and status == "mastered":
            filtered_cards.append(card_data)
        elif filter_status == "Need Review" and status == "review":
            filtered_cards.append(card_data)

    if not filtered_cards:
        st.info(f"No cards with status '{filter_status}' found.")
        return

    # ✅ SPACED REPETITION
    weighted_cards = []
    for card in filtered_cards:
        if card["status"] == "review":
            weighted_cards.extend([card] * 3)
        elif card["status"] == "new":
            weighted_cards.extend([card] * 2)
        else:
            weighted_cards.append(card)

    random.shuffle(weighted_cards)
    filtered_cards = weighted_cards[:len(filtered_cards)]

    # Display cards
    cols = st.columns(3)
    for idx, card in enumerate(filtered_cards):
        col_idx = idx % 3

        with cols[col_idx]:
            card_html = get_flashcard_html(
                card["front"],
                card["back"],
                card["status"],
                f"{card['original_index']}_{idx}"
            )

            components.html(card_html, height=220)

            # Buttons (FIXED)
            btn_col1, btn_col2 = st.columns(2)

            with btn_col1:
                if st.button("Mastered", key=f"master_{card['original_index']}_{idx}"):
                    st.session_state.card_status[card["original_index"]] = "mastered"
                    st.rerun()

            with btn_col2:
                if st.button("Review", key=f"review_{card['original_index']}_{idx}"):
                    st.session_state.card_status[card["original_index"]] = "review"
                    st.rerun()

            # Audio
            if st.button("Play Audio", key=f"audio_{card['original_index']}_{idx}"):
                play_audio(
                    f"{card['front']}. {card['back']}",
                    f"{card['original_index']}_{idx}"
                )

    # Stats
    st.divider()

    total = len(cards)
    mastered = sum(1 for i in range(total) if st.session_state.card_status[i] == "mastered")
    review = sum(1 for i in range(total) if st.session_state.card_status[i] == "review")
    new = sum(1 for i in range(total) if st.session_state.card_status[i] == "new")

    st.write("### Your Progress")

    p_col1, p_col2, p_col3, p_col4 = st.columns(4)
    p_col1.metric("Total Cards", total)
    p_col2.metric("New", new)
    p_col3.metric("Mastered", mastered)
    p_col4.metric("Need Review", review)

    if total > 0:
        progress = mastered / total
        st.progress(progress, text=f"Mastery: {int(progress * 100)}%")