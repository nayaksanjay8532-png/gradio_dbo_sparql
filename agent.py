
from langchain.agents import create_agent

SYSTEM_PROMPT = """
You are a helpful assistant.
If answering requires current or real-world information, use the web_search tool.
Be concise and answer only what is asked.
"""

agent = create_agent(
    model=llm,
    tools=[web_search],
    system_prompt=SYSTEM_PROMPT,
)

# --- Fallback (older LangChain) ---
# from langgraph.prebuilt import create_react_agent
# agent = create_react_agent(llm, tools=[web_search], prompt=SYSTEM_PROMPT)