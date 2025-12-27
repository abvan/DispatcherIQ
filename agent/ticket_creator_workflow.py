from typing import Callable
from langgraph.graph import StateGraph, END
from .workflow_tools import summarize,get_engineer_with_lowest_load,create_ticket,auto_response,send_email
from .state import DispatcherState


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
        graph = StateGraph(DispatcherState)

        # Nodes
        graph.add_node("summarize", summarize)
        graph.add_node("assign", get_engineer_with_lowest_load)
        graph.add_node("create_ticket", create_ticket)
        #graph.add_node("generate_response", auto_response)
        #graph.add_node("send_email", send_email)

        # Flow
        graph.set_entry_point("summarize")
        graph.add_edge("summarize", "assign")
        graph.add_edge("assign", "create_ticket")
        #graph.add_edge("create_ticket", "generate_response")
        #graph.add_edge("generate_response", "send_email")
        graph.add_edge("create_ticket", END)

        return graph.compile()

    def run(self, state: DispatcherState) -> DispatcherState:
        """
        Execute the ticket creator workflow
        """
        return self._graph.invoke(state)

    def as_runnable(self) -> Callable:
        """
        Useful when embedding as a subgraph in another LangGraph
        """
        return self._graph