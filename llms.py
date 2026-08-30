"""
llms.py  --  Inference layer
----------------------------
Two OpenAI-compatible model clients. Keys/URLs come from config.py only.

    llm1 -> Hugging Face Router (gpt-oss-120b)
    llm2 -> Groq (fast inference, drives the agent)
"""

from langchain_openai import ChatOpenAI

from config import (
   GROQ_API_KEY, GROQ_BASE_URL, GROQ_MODEL,
)

# llm : Groq (agent's reasoning engine)
llm = ChatOpenAI(
    base_url=GROQ_BASE_URL,
    api_key=GROQ_API_KEY,
    model=GROQ_MODEL,
    temperature=0,
)
