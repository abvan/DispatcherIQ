from typing import Callable
from langgraph.graph import StateGraph, END
from .tools import summarize,get_engineer_with_lowest_load,create_ticket,auto_response,send_email
from .state import TicektCreatorState


class TicketCreatorGraph:
    """
    Ticket creation subgraph.
    
    Responsibilities:
    - Summarize incoming alert/request
    - Assign engineer
    - Create ticket
    - Generate response
    - Notify user
    """

    def __init__(self):
        self._graph = self._build_graph()

    def _build_graph(self):
        graph = StateGraph(TicektCreatorState)

        # Nodes
        graph.add_node("summarize", summarize)
        graph.add_node("assign", get_engineer_with_lowest_load)
        graph.add_node("create_ticket", create_ticket)

        # Flow
        graph.set_entry_point("summarize")
        graph.add_edge("summarize", "assign")
        graph.add_edge("assign", "create_ticket")
        graph.add_edge("create_ticket", END)

        return graph.compile()

    def run(self, state: TicektCreatorState) -> TicektCreatorState:
        """
        Execute the ticket creator workflow
        """
        return self._graph.invoke(state)

    def as_runnable(self) -> Callable:
        """
        Useful when embedding as a subgraph in another LangGraph
        """
        return self._graph

# RawInput = 'Gross sales margin discrepancy in Power BI report SEF_ALL (production). Observed today. Business impact: Director needs accurate sales figures for closing period. Urgent.'
# input_text = {'Title' : "" , 'Body' : RawInput}
    
# initial_state = {
#     "ticket_id":"",
#     "raw_input":input_text,
#     "severity" : "low",
#     "source":"Email",
#     "classification":'INCIDENT'
# }

#print(TicketCreatorGraph().run(initial_state))
# initial_state = {
#         "raw_input": {
#             "Title": "Issues in PowerBI report",
#             "Body": "Hello operations team , the gross sales margin in the consolidated sales report are not correct when i compare it with the SAP system, could you please check on this ASAP. This is quiet urgent since the Director needs the sales figure in this closing period."
#         },
#         "source": "Email",
#         "classification": {
#                            "category":"",
#                            "sub_category":"",
#                            "severity":"",
#                            "confidence":""
#                            },
#         "severity": "",
#         "assigned_to": "",
#         "next_action": "",
#         "extracted_entities" : "",
#         "status": "received"
#     }    

# print(TicketCreatorGraph().run(initial_state))