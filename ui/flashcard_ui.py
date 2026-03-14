'''import streamlit as st

def display_flashcards(cards):

    st.header("Flashcards")

    for card in cards:
        with st.expander(card["front"]):
            st.write(card["back"])'''
import streamlit as st

def display_flashcards(cards):

    if not cards:
        st.info("No flashcards generated.")
        return

    for i, card in enumerate(cards, start=1):
        with st.expander(f"Flashcard {i}: {card.get('front','Concept')}"):
            st.write(card.get("back", "No definition available"))