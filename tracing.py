"""
tracing.py  --  LangSmith tracing setup
---------------------------------------
Enables LangSmith tracing by exporting the env vars LangChain looks for.
Import and call setup_tracing() ONCE, early -- before the agent is built.

Tracing is OPTIONAL: if LANGSMITH_API_KEY is not set, this quietly does nothing
so the app still runs. Secrets/config come from config.py (the vault boundary).
"""

import os

from config import (
    LANGSMITH_API_KEY,
    LANGSMITH_PROJECT,
    LANGSMITH_ENDPOINT,
)


def setup_tracing() -> bool:
    """Turn on LangSmith tracing if a key is available. Returns True if enabled."""
    if not LANGSMITH_API_KEY:
        # No key -> run without tracing (keeps the app working).
        os.environ["LANGSMITH_TRACING"] = "false"
        return False

    os.environ["LANGSMITH_API_KEY"] = LANGSMITH_API_KEY
    os.environ["LANGSMITH_TRACING"] = "true"
    os.environ["LANGSMITH_PROJECT"] = LANGSMITH_PROJECT
    os.environ["LANGSMITH_ENDPOINT"] = LANGSMITH_ENDPOINT
    return True
