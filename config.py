import os

def load_secret(name: str) -> str:
    """Read a secret from Colab, Streamlit, or plain env vars — whichever is available."""
    # 1) Streamlit Community Cloud
    try:
        import streamlit as st
        if name in st.secrets:
            return st.secrets[name]
    except Exception:
        pass
    # 2) Colab
    try:
        from google.colab import userdata
        val = userdata.get(name)
        if val:
            return val
    except Exception:
        pass
    # 3) Plain environment variables (HF Space, local)
    return os.getenv(name, "")

# --- API keys ---
GROQ_API_KEY   = load_secret("GROQ_API_KEY")
TAVILY_API_KEY = load_secret("TAVILY_API_KEY")

# --- LangSmith tracing config ---
os.environ["LANGSMITH_API_KEY"]  = load_secret("LANGSMITH_API_KEY")
os.environ["LANGSMITH_TRACING"]  = "true"
os.environ["LANGSMITH_PROJECT"]  = "streamlit-groq-tavily-agent"
os.environ["LANGSMITH_ENDPOINT"] = "https://api.smith.langchain.com"

# --- Model config ---
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
GROQ_MODEL    = "qwen/qwen3-32b"