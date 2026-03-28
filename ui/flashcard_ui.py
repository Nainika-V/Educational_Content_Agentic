import streamlit as st
import streamlit.components.v1 as components
import os
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
    # Status colors
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

    # Initialize status if not present
    for card in cards:
        if "status" not in card:
            card["status"] = "new"

    # Filter options
    filter_col1, filter_col2 = st.columns([2, 1])
    with filter_col1:
        st.subheader("Knowledge Flashcards")
    with filter_col2:
        filter_status = st.selectbox(
            "Filter by Status",
            ["All", "New", "Mastered", "Need Review"],
            index=0
        )

    filtered_cards = []
    for i, card in enumerate(cards):
        card["original_index"] = i # Keep track of original index for state updates
        if filter_status == "All":
            filtered_cards.append(card)
        elif filter_status == "New" and card["status"] == "new":
            filtered_cards.append(card)
        elif filter_status == "Mastered" and card["status"] == "mastered":
            filtered_cards.append(card)
        elif filter_status == "Need Review" and card["status"] == "review":
            filtered_cards.append(card)

    if not filtered_cards:
        st.info(f"No cards with status '{filter_status}' found.")
        return

    # Display cards in a grid
    cols = st.columns(3)
    for idx, card in enumerate(filtered_cards):
        col_idx = idx % 3
        with cols[col_idx]:
            # Render individual flashcard
            card_html = get_flashcard_html(
                card.get("front", "Concept"),
                card.get("back", "Definition"),
                card["status"],
                card["original_index"]
            )
            components.html(card_html, height=220)
            
            # Mastered / Review Buttons
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                if st.button("Mastered", key=f"master_{card['original_index']}"):
                    card["status"] = "mastered"
                    st.rerun()
            with btn_col2:
                if st.button("Review", key=f"review_{card['original_index']}"):
                    card["status"] = "review"
                    st.rerun()
            
            # Audio button below
            if st.button(f"Play Audio", key=f"audio_{card['original_index']}"):
                play_audio(f"{card.get('front', '')}. {card.get('back', '')}", card['original_index'])

    # Statistics
    st.divider()
    total = len(cards)
    mastered = len([c for c in cards if c["status"] == "mastered"])
    review = len([c for c in cards if c["status"] == "review"])
    new = len([c for c in cards if c["status"] == "new"])

    st.write("### Your Progress")
    p_col1, p_col2, p_col3, p_col4 = st.columns(4)
    p_col1.metric("Total Cards", total)
    p_col2.metric("New", new)
    p_col3.metric("Mastered ", mastered)
    p_col4.metric("Need Review ", review)

    if total > 0:
        progress = mastered / total
        st.progress(progress, text=f"Mastery: {int(progress * 100)}%")
