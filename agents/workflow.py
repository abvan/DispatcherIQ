from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage

from .workflow_tools import classify,summarize,validate_requirements,get_engineer_with_lowest_load,route_by_classification,send_email
from .state import DispatcherState
from .ticket_creator_agent.ticket_creator import TicketCreatorGraph
#from IPython.display import Image, display


builder = StateGraph(DispatcherState)
builder.add_node("classify", classify)
#builder.add_node("summarize", summarize)
builder.add_node("validate", validate_requirements)
#builder.add_node("assign", get_engineer_with_lowest_load)
builder.add_node("create_ticket", TicketCreatorGraph().run)
builder.add_node("generate_response", send_email)

#builder.add_node("create_ticket", TicketCreatorGraph().run)
# builder.add_node("send_email", send_email)
# builder.set_entry_point("classify")


builder.set_entry_point("classify")
builder.add_conditional_edges(
    "classify",
    route_by_classification,
    {
        "INCIDENT": "create_ticket",
        "REQUEST": "validate",
        "NEED_RESPONSE": "generate_response"
    }
)
#builder.add_edge("summarize", "assign")
#builder.add_edge("assign", "create_ticket")
builder.add_edge("validate", "create_ticket")
# builder.add_edge("generate_response", "send_email")
# builder.add_edge("Summarize_Emails", "create_ticket")
# builder.add_edge("Summarize_Incident", "create_ticket")

#builder.add_edge("send_email",END)

dispatcher_graph = builder.compile()

mermaid = dispatcher_graph.get_graph().draw_mermaid()
print(mermaid)
#display(Image(dispatcher_graph.get_graph().draw_png()))