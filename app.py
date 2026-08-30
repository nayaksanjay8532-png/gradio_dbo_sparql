"""
streamlit_app.py  --  Host entry point (what Streamlit Cloud runs)
------------------------------------------------------------------
Thin Streamlit chat UI. All real work is delegated to run_agent().
Set this filename in Streamlit's "Main File Path" field.
"""

import streamlit as st

from agent import run_agent

st.set_page_config(page_title="Research Assistant Agent", page_icon="🔎")
st.title("🔎 Research Assistant Agent")
st.caption("LangChain agent · Groq inference · Tavily web search · LangSmith tracing")

if "history" not in st.session_state:
    st.session_state.history = []

# Replay past turns
for role, msg in st.session_state.history:
    st.chat_message(role).write(msg)

# Handle new input
if prompt := st.chat_input("Ask me something..."):
    st.session_state.history.append(("user", prompt))
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                reply = run_agent(prompt)
            except Exception as e:
                reply = f"Error: {e}"
            st.write(reply)

    st.session_state.history.append(("assistant", reply))
