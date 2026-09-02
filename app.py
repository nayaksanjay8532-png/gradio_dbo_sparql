"""
app.py  --  Host entry point (what Render runs)
-----------------------------------------------
Thin Gradio chat UI. All real work is delegated to run_agent().
Binds to 0.0.0.0 and the PORT Render provides via env var.
"""

import os

import gradio as gr

from agent import run_agent


def chat_fn(message, history):
    """Called by Gradio for each user turn. `history` is managed by ChatInterface."""
    try:
        return run_agent(message)
    except Exception as e:
        return f"Error: {e}"


demo = gr.ChatInterface(
    fn=chat_fn,
    title="🔎 Research Assistant Agent",
    description="LangChain agent · Groq inference · Tavily web search · LangSmith tracing",
    examples=["What is the current temperature in Mumbai?"],
)

if __name__ == "__main__":
    # Render injects PORT; default 7860 for local runs.
    port = int(os.environ.get("PORT", 7860))
    demo.launch(server_name="0.0.0.0", server_port=port)
