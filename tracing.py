

os.environ["LANGSMITH_API_KEY"]  = load_secret("LANGSMITH_API_KEY")
os.environ["LANGSMITH_TRACING"]  = "true"
os.environ["LANGSMITH_PROJECT"]  = "hf-groq-tavily-agent"
os.environ["LANGSMITH_ENDPOINT"] = "https://api.smith.langchain.com"