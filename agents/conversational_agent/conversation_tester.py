from .conversational_agent import chatgraph
from langchain_core.messages import HumanMessage

# config = {"configurable":{"thread_id":"1"}}
# response = graph.invoke({"messages":"Hi My name is abhishek"},config=config)
# for m in response['messages']:
#     m.pretty_print()

def main():
    graph = chatgraph()

    thread_id = "local_test_user"

    print("Type 'exit' to quit\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        state = {"messages": [HumanMessage(content=user_input)]}

        config = {"configurable": {"thread_id": thread_id}}

        result = graph.invoke(state, config=config)

        print("Bot:", result["messages"][-1].content)

if __name__ == "__main__":
    main()