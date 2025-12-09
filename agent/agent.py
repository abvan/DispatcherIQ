import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_groq import ChatGroq

load_dotenv()

model = ChatGroq(
        model_name="openai/gpt-oss-120b",   # or "llama3-70b-8192"
        groq_api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.2
    )

@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"

@tool
def get_weather(location: str) -> str:
    """Get weather information for a location."""
    return f"Weather in {location}: Sunny, 72°F"

agent = create_agent(
                model, 
                tools=[search, get_weather],
                system_prompt="You are a helpful assistant. Be concise and accurate."
                )

# The system prompt will be set dynamically based on context
result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)

print(result)