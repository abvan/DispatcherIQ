from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage

from .workflow_tools import classify,Summarize_Alerts,Summarize_Emails,get_engineer_with_lowest_load,create_ticket,route_by_classification,auto_response,send_email
from .state import DispatcherState
from IPython.display import Image, display


builder = StateGraph(DispatcherState)
builder.add_node("classify", classify)
builder.add_node("Summarize_Incident", Summarize_Alerts)
builder.add_node("Summarize_Emails", Summarize_Emails)
builder.add_node("create_ticket", create_ticket)
builder.add_node("assign", get_engineer_with_lowest_load)
builder.add_node("generate_response", auto_response)
builder.add_node("send_email", send_email)
builder.set_entry_point("classify")



builder.add_edge("classify", "extract")
# builder.add_conditional_edges(
#     "classify",
#     route_by_classification,
#     {
#         "INCIDENT": "Summarize_Emails",
#         #"CHANGE": "Summarize_Emails", -- Human in Loop Approval
#         "QUERY": "generate_response"
#     }
# )
# builder.add_edge("generate_response", "send_email")
# builder.add_edge("Summarize_Emails", "create_ticket")
# builder.add_edge("Summarize_Incident", "create_ticket")

builder.add_edge("send_email",END)

dispatcher_graph = builder.compile()

mermaid = dispatcher_graph.get_graph().draw_mermaid()
print(mermaid)
#display(Image(dispatcher_graph.get_graph().draw_png()))