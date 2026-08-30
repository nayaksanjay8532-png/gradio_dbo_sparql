
import config          # noqa: F401  (loads keys + LangSmith config on import)
import streamlit as st
from agent import agent

st.set_page_config(page_title="Web-Search Agent", page_icon="🔍")
st.title("🔍 Web-Search Agent (Groq + Tavily)")
st.caption("Ask anything. Uses Tavily for live web info and Groq for fast inference.")

# Keep chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render past messages
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Handle new input
if prompt := st.chat_input("Type your question…"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            result = agent.invoke({"messages": [{"role": "user", "content": prompt}]})
            answer = result["messages"][-1].content
            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})