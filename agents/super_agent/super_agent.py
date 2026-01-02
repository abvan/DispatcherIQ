from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage

from .superagent_tools import email_classification,route_by_classification,create_ticket,validate_requirements,generate_response
from ..state import DispatcherState

#from IPython.display import Image, display


builder = StateGraph(DispatcherState)

## NODES
builder.add_node("classify", email_classification) # classify whether its a ticket creation task, Follow Up , Standard Reqest etc. 
builder.add_node("TicketCreator_Agent",create_ticket)
builder.add_node("validate", validate_requirements)
builder.add_node("Conversation_Agent", generate_response)

## EDGES
builder.set_entry_point("classify")
builder.add_conditional_edges(
    "classify",
    route_by_classification,
    {
        "INCIDENT": "TicketCreator_Agent",
        "REQUEST": "validate",
        "NEED_RESPONSE": "Conversation_Agent"
    }
)

dispatcher_graph = builder.compile()

mermaid = dispatcher_graph.get_graph().draw_mermaid()
print(mermaid)
#display(Image(dispatcher_graph.get_graph().draw_png()))