import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser,PydanticOutputParser

#from langchain_core.messages import HumanMessage,SystemMessage
#from langchain.tools import tool
from pydantic import BaseModel, Field
from typing import Optional, List

from .node_prompts import Email_Classification_prompt,Extract_Alert_Information_Prompt
from .parsing_models import ClassifyEmailOutput,Classification
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


def classify(DispatcherState):
    if DispatcherState['source'] == 'Email' :
        DispatcherState['classification'] = email_intent_classification(email_subject = DispatcherState['raw_input']['Title'],
                                                                        email_body=DispatcherState['raw_input']['Body']
                                                                        )    
        if DispatcherState['classification']["category"] == 'INCIDENT_ANOMALY':
            DispatcherState['classification']["category"] = 'INCIDENT'
    elif DispatcherState['source'] == 'DataDog_Alert' :
        DispatcherState['classification']["category"] = 'INCIDENT'
    elif DispatcherState['source'] == 'Sifflet_Alert' :
        DispatcherState['classification']["category"] = 'INCIDENT'
    else :
        DispatcherState['classification']["category"] = 'INCIDENT' 
    return DispatcherState

def summarize(DispatcherState):
    pass

def Summarize_Alerts(alert_raw_input: str,
                    state : DispatcherState,
                    prompt = [Extract_Alert_Information_Prompt],
                    outputparser = ClassifyEmailOutput,
                    llm = ChatGroq_Model
                   ) -> dict :
    
    if state['next_action'] == 'Create Ticket' :
        if state['source'] == 'DataDog_Alert' :
            parser = PydanticOutputParser(pydantic_object=outputparser) #Check Output Parser for this Alert.
            chain = (prompt[0] | llm | parser)
            response = chain.invoke({{"alert_text": alert_raw_input}})
        
        elif state['source'] == "Email" :
            parser = PydanticOutputParser(pydantic_object=outputparser) #Check Output Parser for this Alert.
            chain = (prompt[0] | llm | parser)
            response = chain.invoke({{"alert_text": alert_raw_input}})
        
        elif state['source'] == "Sifflet_Alert" :
            pass
        
        else :
            pass
    pass

def Summarize_Emails(alert_raw_input: str,
                    state : DispatcherState,
                    prompt = [Extract_Alert_Information_Prompt],
                    outputparser = ClassifyEmailOutput,
                    llm = ChatGroq_Model
                   ) -> dict :
    pass

def get_engineer_with_lowest_load():
    pass

def create_ticket():
    pass


def route_by_classification(state: DispatcherState) -> str:
    
    ##If Email(1st Email) and Incident . -- > Summarize_Email
    ##If Email -> QUERY or Change . -- > Summarize_Email(different parameters)
    ##If Datadog or Sifflet Incident --> Summarize Incident
    classification = state.get("classification")

    if classification == "INCIDENT":
        return "INCIDENT"

    elif classification == "CHANGE":
        return "CHANGE"

    elif classification == "QUERY":
        return "QUERY"

    else:
        return "DEFAULT"
    

def auto_response():
    pass

def send_email() :
    pass