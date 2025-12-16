import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_groq import ChatGroq
from tools import classify_email,get_engineer_with_lowest_load,create_ticket,send_teams_message
from state import AgentState

load_dotenv()

model = ChatGroq(
        model_name="openai/gpt-oss-120b",   # or "llama3-70b-8192"
        groq_api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.2
    )

# Tool definitions
tools = [
    classify_email,
    create_ticket
]

agent = create_agent(
                model, 
                tools=tools,
                system_prompt="""
                    You are an autonomous operations agent.
                    Your job is to fully resolve incoming alerts or email requests.

                    Available tools:
                    - classify_email
                    - create_ticket
                    - notify
                    
                    Use multiple steps if needed.
                    If tool output indicates failure, try a different strategy.
                    Stop only when task is 100 percent completed.
                """
                )

# The system prompt will be set dynamically based on context
result = agent.invoke(
    {"messages": [{"role": "user", "content": "Create a New table from SAP Table named CDPOS in Ceramics CDP"}]}
)

print(result)