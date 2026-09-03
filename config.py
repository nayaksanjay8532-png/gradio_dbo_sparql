"""
config.py  --  Config / secrets boundary
----------------------------------------
Single place that reads secrets & settings from the environment.
On Render, set these as Environment Variables (Dashboard > Environment).
Every other module imports from here, so keys never appear elsewhere.
"""

import os

# --- Groq (inference) ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_BASE_URL = os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1")
GROQ_MODEL = os.getenv("GROQ_MODEL", "qwen/qwen3.8-27b")

# --- Tavily (web search) ---
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
TAVILY_MAX_RESULTS = int(os.getenv("TAVILY_MAX_RESULTS", "5"))

# --- LangSmith (tracing, optional) ---
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT", "research-assistant-agent")
LANGSMITH_ENDPOINT = os.getenv("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")

# --- dbpedia endpoint ---
DBPEDIA_ENDPOINT = "https://dbpedia.org/sparql"
