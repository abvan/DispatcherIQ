from typing import TypedDict, List, Optional,Annotated
from langgraph.graph import StateGraph,START,END
from langchain_core.messages import HumanMessage
from langgraph.graph.message import add_messages
from langchain_core.prompts import ChatPromptTemplate
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver

from .conversational_agent_tools import get_incident_updates,create_ticket
from ..state import DispatcherState
from ..model import ChatGroq_Model
from .prompts import master_prompt

import sqlite3

class State(TypedDict):
    messages:Annotated[list,add_messages]

tools = [get_incident_updates,create_ticket]

llm_with_tools = ChatGroq_Model.bind_tools(tools)


## Node definition
def tool_calling_llm(state:State, llm_with_tools=llm_with_tools, prompt = master_prompt):
    chain = prompt | llm_with_tools
    return {"messages":[chain.invoke(state["messages"])]}

def chatgraph():
    ## Graph
    builder=StateGraph(State)
    builder.add_node("tool_calling_llm",tool_calling_llm)
    builder.add_node("tools",ToolNode(tools))

    ## Add Edges
    builder.add_edge(START, "tool_calling_llm")
    builder.add_conditional_edges(
        "tool_calling_llm",
        tools_condition
    )
    builder.add_edge("tools","tool_calling_llm")

    conn = sqlite3.connect('langgraphagent.db',check_same_thread=False)
    memory = SqliteSaver(conn)

    ## compile the graph
    return builder.compile(checkpointer=memory)