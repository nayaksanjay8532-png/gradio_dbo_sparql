
"""
tools.py  --  Agent tools
-------------------------
Small, self-contained capabilities the agent can call. Add more here and they
are picked up automatically via the ALL_TOOLS registry.
"""

from langchain.tools import tool
from tavily import TavilyClient

from config import TAVILY_API_KEY, TAVILY_MAX_RESULTS

_tavily_client = TavilyClient(api_key=TAVILY_API_KEY)


@tool
def web_search(query: str) -> str:
    """Search the web using Tavily and return the raw result."""
    result = _tavily_client.search(query=query, max_results=TAVILY_MAX_RESULTS)
    return str(result)


ALL_TOOLS = [web_search]
