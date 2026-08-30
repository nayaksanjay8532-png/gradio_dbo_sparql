
from langchain.tools import tool
from tavily import TavilyClient

tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

@tool
def web_search(query: str) -> str:
    """Search the web for current information using Tavily."""
    result = tavily_client.search(query=query, max_results=3)
    return str(result)