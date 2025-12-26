import os
import json
from datetime import datetime,timezone
import uuid
import pandas as pd
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser,PydanticOutputParser

#from langchain_core.messages import HumanMessage,SystemMessage
#from langchain.tools import tool
from pydantic import BaseModel, Field
from typing import Optional, List

from .node_prompts import Email_Classification_prompt,Summarize_Alert_Incident
from .parsing_models import ClassifyEmailOutput,Classification,AlertIncidentSummary
from .state import DispatcherState


load_dotenv()

ChatGroq_Model = ChatGroq(
    model_name="openai/gpt-oss-120b",   # or "llama3-70b-8192"
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.2
)


def email_intent_classification(email_subject: str,
                   email_body: str,
                   thread_id: Optional[str] = None,
                   prompt = Email_Classification_prompt,
                   outputparser = Classification,
                   llm = ChatGroq_Model
                   ) -> dict :  
    #"""Classifies an email for Operations dispatching."""    
    parser = PydanticOutputParser(pydantic_object=outputparser)    
    chain = (prompt | llm | parser)
    ClassifyEmailOutput = chain.invoke({
            "subject": email_subject,
            "body": email_body,
            "thread_id": thread_id or "None",
            "format_instructions": parser.get_format_instructions()
        })
    return ClassifyEmailOutput.model_dump()


def classify(state: DispatcherState):
    if state['source'] == 'Email' :
        state['classification'] = email_intent_classification(email_subject = state['raw_input']['Title'],
                                                                        email_body = state['raw_input']['Body']
                                                                        )    
        if state['classification']['category'] == 'INCIDENT_ANOMALY':
            state['classification']['category'] = 'INCIDENT'
    elif state['source'] == 'DataDog' :
        state['classification']['category'] = 'INCIDENT'
    elif state['source'] == 'Sifflet' :
        state['classification']['category'] = 'INCIDENT'
    else :
        state['classification']['category'] = 'INCIDENT' 
    return state






def route_by_classification(state: DispatcherState) -> str: 
    if state['classification']['category'] in ('INCIDENT'):
        return "INCIDENT"
    if state['classification']['category'] in ('STANDARD_REQUEST','CHANGE_REQUEST','ACCESS_REQUEST'):
        return "REQUEST"
    elif state['classification']['category'] in ('QUERY','FOLLOW_UP','QUESTION'):
        return "NEED_RESPONSE"
    else:
        return "DEFAULT"


def Summarize_Alerts(state : DispatcherState,
                    prompt = [Summarize_Alert_Incident],
                    outputparser = AlertIncidentSummary,
                    llm = ChatGroq_Model
                   ) -> dict :

    if state['source'] == 'DataDog' :
        parser = PydanticOutputParser(pydantic_object=outputparser) #Check Output Parser for this Alert.
        chain = (prompt[0] | llm | parser)
        response = chain.invoke({"alert_text": (state['raw_input']['Title'] + state['raw_input']['Body']),
                                 "format_instructions": parser.get_format_instructions()})
        state['summary'] = response.model_dump_json(indent=2)
        return state
    elif state['source'] == "Sifflet_Alert" :
        pass

def Summarize_Emails(state : DispatcherState, 
                     prompt = Summarize_Alert_Incident, 
                     outputparser = ClassifyEmailOutput,
                     llm = ChatGroq_Model) -> dict :
    
    pass

def summarize(state: DispatcherState):
    print("Summarizing Incident......")
    if state['source'] == 'Email':
        abc = Summarize_Emails()
        #UpdateState

    if state['source'] in ('DataDog','Sifflet'):
        abc = Summarize_Alerts(state)
        #UpdateState

    return abc

def get_engineer_with_lowest_load(state: DispatcherState) -> dict:
    print(state)
    return state


def format_raw_incident_for_ticket(raw_incident: dict) -> str:
    lines = []
    lines.append("Incident Title:")
    lines.append(raw_incident.get("Title", "N/A"))
    lines.append("")
    lines.append("Incident Description:")
    lines.append(raw_incident.get("Body", "N/A"))
    return "\n".join(lines)

def format_summary_for_ticket(json_str: str) -> str:
    data = json.loads(json_str)

    output = []
    output.append(f"Summary:\n{data.get('summary')}\n")
    output.append(f"Root Cause:\n{data.get('root_cause_explanation')}\n")

    output.append("Possible Solutions:")
    for i, sol in enumerate(data.get("possible_solutions", []), 1):
        output.append(f"  {i}. {sol}")

    output.append("\nNext Recommended Actions:")
    for i, act in enumerate(data.get("next_recommended_actions", []), 1):
        output.append(f"  {i}. {act}")

    return "\n".join(output)

 #Agentic tool to create a ticket and persist it as a row in Excel.
def create_ticket(state: DispatcherState) -> dict:
      
    excel_path = "tickets.xlsx"
    
    # Generate ticket metadata 
    ticket_id = f"TCK-{uuid.uuid4().hex[:8].upper()}"
    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


    # Extract from agent state
    raw_incident = state.get("raw_input", {})
    classification = state.get("classification", {})
    
    severity = classification.get("severity")
    sla_mapping = {
        "P1": 4,
        "P2": 8,
        "P3": 24
    }

    ticket_row = {
        "ticket_id": ticket_id,
        "created_at": created_at,
        "source": state.get("source"),
        "category": classification.get("category"),
        "sub_category": classification.get("sub_category"),
        "severity": severity,
        "raw_incident": format_raw_incident_for_ticket(raw_incident),
        "AI_Incident_summary": format_summary_for_ticket(state.get("summary")),
        "assigned_engineer": state.get("assigned_to"),
        "next_action": state.get("next_action"),
        "sla_hours": sla_mapping.get(severity),
        "status": "OPEN",
        "Engineer_Updates" : "",
        "closing_time" : ""
    }


    # --- Persist to Excel ---
    if os.path.exists(excel_path):
        df = pd.read_excel(excel_path)
        df = pd.concat([df, pd.DataFrame([ticket_row])], ignore_index=True)
    else:
        df = pd.DataFrame([ticket_row])

    df.to_excel(excel_path, index=False)

    # --- Update state with ticket_id ---
    state["ticket_id"] = ticket_id

    return state


def validate_requirements():
    ##If we have a ('STANDARD_REQUEST','CHANGE_REQUEST','ACCESS_REQUEST') : This function should check all the required data for each 
    # and ask the user to provide the information if they are insufficient
    pass





def auto_response():
    pass

def send_email() :
    pass