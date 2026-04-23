import streamlit as st
import asyncio
import os
import sys

# Add the scripts directory to the path so we can import the agent
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from home_admin_agent import HomeAdminAgent

st.set_page_config(page_title="Ralph - Home Admin Agent", page_icon="🤖")

st.title("🤖 Ralph - Home Admin Agent")
st.markdown("Your autonomous homelab assistant. Ask me about tasks, schedules, or home automation.")

# Initialize the agent
@st.cache_resource
def get_agent():
    return HomeAdminAgent()

agent = get_agent()

# Initialize chat history from agent memory if empty
if "messages" not in st.session_state or not st.session_state.messages:
    with st.spinner("Loading history..."):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        history = loop.run_until_complete(agent.get_history())
        st.session_state.messages = history

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What can I help you with today?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Ralph is thinking..."):
            # Run the agent in an async loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            response = loop.run_until_complete(agent.run(prompt))

            if response:
                st.markdown(response)
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
            else:
                st.error("I'm sorry, I encountered an error processing your request.")

# Sidebar info
with st.sidebar:
    st.header("Voice Interface")
    voice_enabled = st.toggle("Enable Voice (Hands-free mode)", value=False)
    if voice_enabled:
        st.info("Voice interface active. (STT/TTS integration TBD)")

    st.header("Document Ingestion")
    uploaded_file = st.file_uploader("Upload a document for Paperless-ngx", type=["pdf", "png", "jpg", "txt"])
    if uploaded_file:
        st.success(f"File {uploaded_file.name} received! (Ingestion logic TBD)")

    st.header("Capabilities")
    st.write("Current tools registered:")
    for tool in agent.registry.list_tools():
        st.write(f"- **{tool.name}**: {tool.description}")

    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
