import pandas as pd
from ..ticket_creator_agent.ticket_creator import TicketCreatorGraph
from .prompts import ticket_updates_prompt
from ..model import ChatGroq_Model

def get_ticket_comments(ticket_number: str):
    
    excel_path = "tickets.xlsx"
    comments_column = "Engineer_Updates"
    ticket_column = "ticket_id"

    df = pd.read_excel(excel_path)
    ticket_rows = df[df[ticket_column] == ticket_number]
    
    if ticket_rows.empty:
        return "No Comments"

    # Drop null comments and return as list
    comments = "\n".join(
        ticket_rows[comments_column]
        .dropna()
        .astype(str)
        .tolist()
    )
    return comments

def get_incident_updates(ticket_number:str,prompt = ticket_updates_prompt) -> str:
    """This Function give us the engineer comments and progress on the incident ticket"""
    comments = get_ticket_comments(ticket_number)
    chain = prompt | ChatGroq_Model
    response = chain.invoke([comments])
    return response.content


def create_ticket(RawInput:str) -> str:
    """This function creates a new ticket an assigns it to an engineer and returns the ticket number"""
    input_text = {'Title' : "" , 'Body' : RawInput}
    
    initial_state = {
        "ticket_id":"",
        "raw_input":input_text,
        "severity" : "low",
        "source":"Email",
        "classification":'INCIDENT'
    }
    response_state = TicketCreatorGraph().run(initial_state)
    return response_state


