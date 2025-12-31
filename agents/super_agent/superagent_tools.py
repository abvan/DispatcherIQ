from langchain_core.output_parsers import PydanticOutputParser
from .prompts import Email_Classification_prompt
from .superagent_state import DispatcherState
from ..pydantic_outputparsers.outputparsers import Email_Classification
from ..model import ChatGroq_Model
from ..ticket_creator_agent.ticket_creator import TicketCreatorGraph

## email_intent_classification
## Retrive the previous conversation of the same mail thread
## Classify the recent mail
## Update the state for next actions

def email_classification(state: DispatcherState, prompt = Email_Classification_prompt, outputparser = Email_Classification, llm = ChatGroq_Model ) -> dict :  
    #"""Classifies an email for Operations dispatching."""    
    email_subject = state['raw_input']['Title'] 
    email_body = state['raw_input']['Body']
    parser = PydanticOutputParser(pydantic_object=outputparser)    
    chain = (prompt | llm | parser)
    emailClassification = chain.invoke({
            "subject": email_subject,
            "body": email_body,
            "format_instructions": parser.get_format_instructions()
        })
    state['classification'] = emailClassification
    print(state)
    return state

# state = DispatcherState(
#     raw_input = {
#         "Title" : "Issues in PowerBI report",
#         "Body" : "Hello operations team , the gross sales margin in the consolidated sales report are not correct when i compare it with the SAP system, could you please check on this ASAP. This is quiet urgent since the Director needs the sales figure in this closing period."
#     }
# )


def route_by_classification(state: DispatcherState) -> str: 
    if state['classification'].category in ('INCIDENT'):
        return "INCIDENT"
    if state['classification'].category in ('STANDARD_REQUEST','CHANGE_REQUEST','ACCESS_REQUEST'):
        return "REQUEST"
    elif state['classification'].category in ('QUERY','FOLLOW_UP','QUESTION'):
        return "NEED_RESPONSE"
    else:
        return "DEFAULT"


# state = DispatcherState(
#     raw_input = {
#         "Title" : "Issues in PowerBI report",
#         "Body" : "Hello operations team , the gross sales margin in the consolidated sales report are not correct when i compare it with the SAP system, could you please check on this ASAP. This is quiet urgent since the Director needs the sales figure in this closing period."
#     }
# )
#print(email_classification(state=state))


 #Agentic tool to create a ticket and persist it as a row in Excel.
def create_ticket(state: DispatcherState) -> dict:    
    initial_state = {
        "ticket_id":"",
        "raw_input":state['raw_input'],
        "source":"Email",
        "classification":state['classification']
    }
    print(initial_state)
    response_state =  TicketCreatorGraph().run(initial_state)
    return response_state



#print(create_ticket(state))