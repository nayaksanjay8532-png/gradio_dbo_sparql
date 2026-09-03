
"""
tools.py  --  Agent tools
-------------------------
Small, self-contained capabilities the agent can call. Add more here and they
are picked up automatically via the ALL_TOOLS registry.
"""

from langchain.tools import tool
from tavily import TavilyClient

import json
from SPARQLWrapper import SPARQLWrapper, JSON

from config import TAVILY_API_KEY, TAVILY_MAX_RESULTS, DBPEDIA_ENDPOINT

_tavily_client = TavilyClient(api_key=TAVILY_API_KEY)


@tool
def web_search(query: str) -> str:
    """Search the web using Tavily and return the raw result."""
    result = _tavily_client.search(query=query, max_results=TAVILY_MAX_RESULTS)
    return str(result)

@tool
def dbpedia_sparql(query: str) -> str:
    """
    Execute a SPARQL query against the public DBpedia endpoint
    (https://dbpedia.org/sparql) and return the results.

    Input:
        query : a COMPLETE, valid SPARQL SELECT query string
                (include all PREFIX declarations).
    Output:
        JSON string of the result rows (variable -> value).
    """
    try:
        sparql = SPARQLWrapper(DBPEDIA_ENDPOINT)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        sparql.addCustomHttpHeader("User-Agent", "DBpedia-LangChain-Agent/1.0")
        sparql.setTimeout(30)

        raw = sparql.query().convert()
        rows = raw.get("results", {}).get("bindings", [])

        # Flatten each binding to a simple {var: value} dict
        cleaned = [
            {var: cell.get("value") for var, cell in row.items()}
            for row in rows
        ]
        if not cleaned:
            return "No results found. Check the actor URI or property names."
        return json.dumps(cleaned, ensure_ascii=False, indent=2)

    except Exception as e:
        return f"SPARQL execution error: {e}"


ALL_TOOLS = [web_search,dbpedia_sparql]
