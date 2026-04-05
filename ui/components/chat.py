import streamlit as st
from core.engine import run_agent_query

def chat_interface():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Check if agent is ready
    if "agent_executor" not in st.session_state:
        st.info("Please upload a document to start the conversation.")
        return None

    # React to user input
    if prompt := st.chat_input("Ask something about the document..."):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    history = []
                    for m in st.session_state.messages[:-1]: 
                        role = "human" if m["role"] == "user" else "ai"
                        history.append((role, m["content"]))

                    response = run_agent_query(st.session_state.agent_executor, prompt, history)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
                    return None
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
        return st.session_state.messages[-1]["content"]
    
    return None
