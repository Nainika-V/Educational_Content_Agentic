import streamlit as st
import sys
import os

# Add the project root to the python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from ui.components.header import show_header
from ui.components.sidebar import show_sidebar
from ui.components.chat import chat_interface
from ui.styles.css import load_css


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
