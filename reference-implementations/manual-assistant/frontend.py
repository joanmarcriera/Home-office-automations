import streamlit as st
import requests
import os

# Configuration
BACKEND_URL = os.environ.get("MANUAL_ASSISTANT_BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="Manual Assistant", page_icon="📖", layout="wide")

st.title("📖 AI-Powered Manual Assistant")
st.write("Troubleshoot your household appliances using scanned manuals.")

# Sidebar for filters
st.sidebar.header("Filters & Settings")
manufacturer = st.sidebar.text_input("Manufacturer (optional)", placeholder="e.g. Bosch")
model_number = st.sidebar.text_input("Model Number (optional)", placeholder="e.g. SHP878ZD5N")
top_k = st.sidebar.slider("Number of context chunks", min_value=1, max_value=10, value=5)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message and message["sources"]:
            with st.expander("View Sources"):
                for i, source in enumerate(message["sources"]):
                    st.write(f"**Source {i+1}:** {source['metadata'].get('section', 'Unknown Section')}")
                    st.write(source['text'])
                    st.divider()

# React to user input
if prompt := st.chat_input("How do I clean the filter?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Searching manuals..."):
            try:
                payload = {
                    "query": prompt,
                    "manufacturer": manufacturer if manufacturer else None,
                    "model_number": model_number if model_number else None,
                    "top_k": top_k
                }
                response = requests.post(f"{BACKEND_URL}/ask", json=payload)
                response.raise_for_status()
                data = response.json()

                answer = data["answer"]
                sources = data["sources"]

                st.markdown(answer)

                if sources:
                    with st.expander("View Sources"):
                        for i, source in enumerate(sources):
                            st.write(f"**Source {i+1}:** {source['metadata'].get('section', 'Unknown Section')} (Score: {source['score']:.4f})")
                            st.write(source['text'])
                            st.divider()

                # Add assistant response to chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })
            except Exception as e:
                st.error(f"Error connecting to backend: {e}")

st.divider()
st.caption("Home-Office Automation - Manual Assistant v1.0")
