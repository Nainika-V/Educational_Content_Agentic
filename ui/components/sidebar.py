import streamlit as st
import os

UPLOAD_FOLDER = "uploaded_docs"

def show_sidebar():

    with st.sidebar:

        st.title("Controls")

        uploaded_file = st.file_uploader(
            "Upload PDF",
            type=["pdf"]
        )

        if uploaded_file:

            os.makedirs(UPLOAD_FOLDER, exist_ok=True)

            file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)

            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.success("File uploaded successfully")

        return uploaded_file