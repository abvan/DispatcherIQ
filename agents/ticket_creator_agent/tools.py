
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

from ..node_prompts import Summarize_Alert_Incident
from ..parsing_models import ClassifyEmailOutput,AlertIncidentSummary
from .state import TicektCreatorState

load_dotenv()

ChatGroq_Model = ChatGroq(
    model_name="openai/gpt-oss-120b",   # or "llama3-70b-8192"
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.2
)

def Summarize_Alerts(state : TicektCreatorState,
                    prompt = Summarize_Alert_Incident,
                    outputparser = AlertIncidentSummary,
                    llm = ChatGroq_Model
                   ) -> dict :

    if state['source'] == 'DataDog' :
        parser = PydanticOutputParser(pydantic_object=outputparser) #Check Output Parser for this Alert.
        chain = (prompt | llm | parser)
        response = chain.invoke({"alert_text": (state['raw_input']['Title'] + state['raw_input']['Body']),
                                 "format_instructions": parser.get_format_instructions()})
        state['summary'] = response.model_dump_json(indent=2)
        return state
    elif state['source'] == "Sifflet_Alert" :
        pass

def Summarize_Emails(state : TicektCreatorState, 
                     prompt = Summarize_Alert_Incident, 
                     outputparser = ClassifyEmailOutput,
                     llm = ChatGroq_Model) -> dict :
    
    pass

def summarize(state: TicektCreatorState):
    print("Summarizing Incident......")
    if state['source'] == 'Email':
        abc = Summarize_Emails(state)
        #UpdateState

    if state['source'] in ('DataDog','Sifflet'):
        abc = Summarize_Alerts(state)
        #UpdateState

    return abc

def get_engineer_with_lowest_load(state: TicektCreatorState) -> dict:
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
    if json_str is None:
        return ""
    else:
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
def create_ticket(state: TicektCreatorState) -> dict:
    excel_path = "tickets.xlsx"
    
    # Generate ticket metadata 
    ticket_id = f"TCK-{uuid.uuid4().hex[:8].upper()}"
    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


    # Extract from agent state
    raw_incident = state.get("raw_input", {})
    classification = state.get("classification", {})
    
    severity = classification.severity
    sla_mapping = {
        "P1": 4,
        "P2": 8,
        "P3": 24
    }

    ticket_row = {
        "ticket_id": ticket_id,
        "created_at": created_at,
        "source": state["source"],
        "category": classification.category,
        "sub_category": classification.sub_category,
        "severity": severity,
        "raw_incident": format_raw_incident_for_ticket(raw_incident),
        "AI_Incident_summary": format_summary_for_ticket(state.get('summary')),
        "assigned_engineer": state.get("assigned_to"),
        "sla_hours": sla_mapping.get('severity'),
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



def auto_response():
    pass

def send_email() :
    pass