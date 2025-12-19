from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage

from workflow_tools import intent_classification,Summarize_Alerts
from state import DispatcherState
from IPython.display import Image, display


builder = StateGraph(DispatcherState)
builder.add_node("classify", intent_classification)
builder.add_node("extract", Summarize_Alerts)
# builder.add_node("ticket", create_ticket)
# builder.add_node("assign", assign_owner)
# builder.add_node("respond", generate_response)


builder.set_entry_point("classify")


builder.add_edge("classify", "extract")
builder.add_edge("extract",END)
# builder.add_edge("extract", "ticket")
# builder.add_edge("ticket", "assign")
# builder.add_edge("assign", "respond")
# builder.add_edge("respond", END)

dispatcher_graph = builder.compile()

mermaid = dispatcher_graph.get_graph().draw_mermaid()
print(mermaid)
#display(Image(dispatcher_graph.get_graph().draw_png()))