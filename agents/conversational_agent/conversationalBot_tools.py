from ..ticket_creator_agent.ticket_creator import TicketCreatorGraph

def get_incident_updates(ticket_number:str) -> str:
    """This Function give us the engineer comments and progress on the incident ticket"""
    return "In Progress"
    pass

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


