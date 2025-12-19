import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser,PydanticOutputParser

#from langchain_core.messages import HumanMessage,SystemMessage
#from langchain.tools import tool
from pydantic import BaseModel, Field
from typing import Optional, List

from node_prompts import Email_Classification_prompt,Extract_Alert_Information_Prompt
from parsing_models import ClassifyEmailOutput
from state import DispatcherState

load_dotenv()

ChatGroq_Model = ChatGroq(
    model_name="openai/gpt-oss-120b",   # or "llama3-70b-8192"
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.2
)

def intent_classification(email_subject: str,
                   email_body: str,
                   thread_id: Optional[str] = None,
                   prompt = Email_Classification_prompt,
                   outputparser = ClassifyEmailOutput,
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

    #UPDATE THE STATE OBJECT
    #..........

    #PERSIST THE STATE IN DATEBASE
    #...........
    
    return ClassifyEmailOutput.model_dump()


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


def get_engineer_with_lowest_load():
    pass

def create_ticket():
    pass
