
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ["GROQ_API_KEY"],
    #model="qwen/qwen3-32b",   # pick a current Groq-hosted model
    model="qwen/qwen3.8-27b",
    temperature=0,
)