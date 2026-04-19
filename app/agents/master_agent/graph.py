from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition

from typing import TypedDict,Annotated

from ...tools.base_tools import get_tools
from .prompts.build_prompt import get_master_prompt
from ...llm.llm_factory import LLMFactory

tools = [get_tools]

# State definition
class State(TypedDict):
    messages:Annotated[list,add_messages]

llm_with_tools = LLMFactory().get_llm("chatgroq").bind_tools(tools)

## Node definition
def tool_calling_llm(state:State, llm_with_tools=llm_with_tools, prompt = get_master_prompt()):
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
    builder.add_edge(END,"tool_calling_llm")

    # conn = sqlite3.connect('langgraphagent.db',check_same_thread=False)
    # memory = SqliteSaver(conn)

    # ## compile the graph
    # return builder.compile() #checkpointer=memory