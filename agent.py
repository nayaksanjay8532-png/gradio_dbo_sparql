"""
agent.py  --  Agent logic
-------------------------
Wires model + tools + system prompt into one agent and exposes run_agent().
Tracing is enabled here (before the agent is built) so all runs are captured.
"""

from langchain.agents import create_agent

from tracing import setup_tracing   # enable LangSmith BEFORE building the agent
from llms import llm
from tools import ALL_TOOLS

# Turn on tracing (no-op if LANGSMITH_API_KEY isn't set).
setup_tracing()

SYSTEM_PROMPT = """
You are a helpful assistant.

If information requires a web search, use the web_search tool.
"""


def build_agent():
    """Construct the agent (model=Groq llm2 + web_search tool)."""
    return create_agent(
        model=llm,
        tools=ALL_TOOLS,
        system_prompt=SYSTEM_PROMPT,
    )


# Build once (not on every request).
agent = build_agent()


def run_agent(user_text: str) -> str:
    """Send one user message to the agent and return the final text reply."""
    response = agent.invoke(
        {"messages": [{"role": "user", "content": user_text}]}
    )
    return response["messages"][-1].content


if __name__ == "__main__":
    # Local smoke test:  python agent.py
    print(run_agent("What is the current temperature in Mumbai? Temperature only."))
