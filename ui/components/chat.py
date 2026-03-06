import streamlit as st

def chat_interface():

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.write(message["content"])

    prompt = st.chat_input("Ask something about the document...")

    if prompt:

        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        with st.chat_message("user"):
            st.write(prompt)

        # Placeholder response (backend will replace this)
        response = "Answer will come from the RAG system."

        with st.chat_message("assistant"):
            st.write(response)

        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )