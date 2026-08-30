"""
config.py  --  The single "Secrets Vault" boundary
--------------------------------------------------
The ONLY module that reads credentials. Everyone else imports names from here.

Secret resolution order (works everywhere):
    1. st.secrets   -> Streamlit Cloud (Manage app -> Settings -> Secrets, TOML)
    2. os.environ   -> Hugging Face Space Secrets / local .env / Colab
This means the exact same code runs on Streamlit, HF, and locally with no edits.
"""

import os

# Optional local .env support (does nothing on Streamlit/HF, which is fine).
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Optional Streamlit secrets support (only present when running under Streamlit).
try:
    import streamlit as st
    _ST_SECRETS = dict(st.secrets)
except Exception:
    _ST_SECRETS = {}


def load_secret(name: str, required: bool = True, default: str | None = None) -> str | None:
    """Fetch a secret from Streamlit secrets first, then environment variables."""
    value = _ST_SECRETS.get(name) or os.getenv(name) or default
    if required and not value:
        raise EnvironmentError(
            f"Missing secret '{name}'. Add it in Streamlit -> Settings -> Secrets "
            f"(TOML), HF -> Settings -> Secrets, or a local .env file."
        )
    return value


# ---- Secrets ----
# HF_TOKEN        = load_secret("HF_TOKEN")
GROQ_API_KEY    = load_secret("GROQ_API_KEY")
TAVILY_API_KEY  = load_secret("TAVILY_API_KEY")
LANGSMITH_API_KEY = load_secret("LANGSMITH_API_KEY", required=False)  # tracing optional

# ---- Non-sensitive config (safe defaults; override via env/Variables) ----
# HF_BASE_URL   = load_secret("HF_BASE_URL",   required=False, default="https://router.huggingface.co/v1")
GROQ_BASE_URL = load_secret("GROQ_BASE_URL", required=False, default="https://api.groq.com/openai/v1")

# HF_MODEL   = load_secret("HF_MODEL",   required=False, default="openai/gpt-oss-120b")
GROQ_MODEL = load_secret("GROQ_MODEL", required=False, default="qwen/qwen3.8-27b")  # confirm exact ID in Groq console

TAVILY_MAX_RESULTS = int(load_secret("TAVILY_MAX_RESULTS", required=False, default="1"))

# LangSmith config (non-secret parts)
LANGSMITH_PROJECT  = load_secret("LANGSMITH_PROJECT",  required=False, default="hf-groq-tavily-agent")
LANGSMITH_ENDPOINT = load_secret("LANGSMITH_ENDPOINT", required=False, default="https://api.smith.langchain.com")
