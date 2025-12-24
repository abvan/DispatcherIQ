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


def classify(state: DispatcherState):
    if state['source'] == 'Email' :
        state['classification'] = email_intent_classification(email_subject = state['raw_input']['Title'],
                                                                        email_body = state['raw_input']['Body']
                                                                        )    
        if state['classification']['category'] == 'INCIDENT_ANOMALY':
            state['classification']['category'] = 'INCIDENT'
    elif state['source'] == 'DataDog_Alert' :
        state['classification']['category'] = 'INCIDENT'
    elif state['source'] == 'Sifflet_Alert' :
        state['classification']['category'] = 'INCIDENT'
    else :
        state['classification']['category'] = 'INCIDENT' 
    print(state)
    return state


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

def summarize(state: DispatcherState):
    if state['source'] == 'Email':
        abc = Summarize_Emails()
        #UpdateState

    if state['source'] in ('DataDog','Sifflet'):
        abc = Summarize_Alerts(state['raw_input'])
        #UpdateState

    return state



def route_by_classification(state: DispatcherState) -> str: 
    if state['classification']['category'] in ('INCIDENT'):
        return "INCIDENT"
    if state['classification']['category'] in ('STANDARD_REQUEST','CHANGE_REQUEST','ACCESS_REQUEST'):
        return "VALIDATE"
    elif state['classification']['category'] in ('QUERY','FOLLOW_UP','QUESTION'):
        return "RESPONSE_USER"
    else:
        return "DEFAULT"
    
def validate_requirements():
    ##If we have a ('STANDARD_REQUEST','CHANGE_REQUEST','ACCESS_REQUEST') : This function should check all the required data for each 
    # and ask the user to provide the information if they are insufficient
    pass

def get_engineer_with_lowest_load():
    pass

def create_ticket():
    pass

def auto_response():
    pass

def send_email() :
    pass