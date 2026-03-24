from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.tools import tool


model_text_deepseek = 'deepseek/deepseek-r1-0528-qwen3-8b'

llm_url = "http://localhost:1234/v1"

deepseek_model = ChatOpenAI(
    base_url=llm_url,
    model=model_text_deepseek,
    temperature=0.2)

@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"

@tool
def get_weather(location: str) -> str:
    """Get weather information for a location."""
    return f"Weather in {location}: Sunny, 72°F"

agent = create_agent(deepseek_model,tools=[search, get_weather])

