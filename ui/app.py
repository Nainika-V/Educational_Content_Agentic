import streamlit as st

from components.header import show_header
from components.sidebar import show_sidebar
from components.chat import chat_interface
from styles.css import load_css


st.set_page_config(
    page_title="Educational AI Agent",
    page_icon="📚",
    layout="wide"
)

st.markdown(load_css(), unsafe_allow_html=True)

show_header()

uploaded_file = show_sidebar()

if uploaded_file:
    st.success("PDF uploaded successfully!")

chat_interface()