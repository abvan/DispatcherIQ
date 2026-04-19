from langchain_core.prompts import ChatPromptTemplate
from app.utils.prompt_loader import load_prompt

def get_master_prompt():
    path = "app/agents/master_agent/prompts/master_prompt.yaml"
    agent_prompt = load_prompt(path)

    return ChatPromptTemplate.from_messages([
        ("system", agent_prompt["master_agent"]["system"]),
        ("human", agent_prompt["master_agent"]["human"])
    ])