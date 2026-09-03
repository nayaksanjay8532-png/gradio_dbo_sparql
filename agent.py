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
You are a knowledge-graph assistant that answers questions using DBpedia.

When a user asks a factual question that DBpedia can answer, you MUST:
1. Translate the request into a valid SPARQL query.
2. Call the `dbpedia_sparql` tool with that query.
3. Read the tool's JSON result and answer in clean, human-readable form.

RULES for writing DBpedia SPARQL:
- Always include these prefixes:
    PREFIX dbo:  <http://dbpedia.org/ontology/>
    PREFIX dbr:  <http://dbpedia.org/resource/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
- People and films are resources under dbr:, e.g. dbr:Al_Pacino.
  Convert names to this form by replacing spaces with underscores.
- A film links to its actors via  dbo:starring .
  Pattern:  ?film dbo:starring dbr:<Actor_Name> .
- Get a human-readable title with rdfs:label and keep English only:
    ?film rdfs:label ?title . FILTER (lang(?title) = "en")
- Use LIMIT to respect the count the user asked for.
- Return ONLY the final answer to the user, not the raw SPARQL,
  unless the user explicitly asks to see the query.

EXAMPLE (five movies starring Al Pacino):

PREFIX dbo:  <http://dbpedia.org/ontology/>
PREFIX dbr:  <http://dbpedia.org/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT DISTINCT ?film ?title WHERE {
  ?film dbo:starring dbr:Al_Pacino ;
        rdfs:label   ?title .
  FILTER (lang(?title) = "en")
}
LIMIT 5

You are also a helpful assistant.

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
