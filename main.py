from fastapi import FastAPI,Request
from pydantic import BaseModel
from typing import Any

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import asynccontextmanager
from datetime import datetime

from langchain_core.messages import HumanMessage
from agents.ticket_creator_agent.ticket_creator import TicketCreatorGraph
from agents.conversational_agent.conversational_agent import chatgraph
import psycopg2


# scheduler = AsyncIOScheduler()

# def my_cron_job():
#     print("Cron job executed:", datetime.now())

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     scheduler.start() # Start scheduler
#     scheduler.add_job(  # Add cron job (every 5 minutes)
#         my_cron_job,
#         trigger="cron",
#         second ="*/10"
#     )
#     print("Scheduler started")
#     yield
#     print("Shutting down scheduler")
#     scheduler.shutdown()

# app = FastAPI(lifespan=lifespan)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello":"sexy"}




# Request body model
class DataDogAlert(BaseModel):
    ddsource : str
    event_type : str
    alert_title: str
    alert_priority: str
    tags : Any
    event : Any

class EmailAlert(BaseModel):
    Subject : str
    Body : str
    thread_id : str


##------------------------ POST endpoints(alerts Monitor (Webhooks))----------------------------------##
@app.post("/Email_Monitor")
async def create_item(alert: EmailAlert):
    
    config = {
        "configurable": {
            "thread_id": alert.thread_id #req.thread_id
        }
    }
    
    state = {
        "messages": [HumanMessage(content=alert.Body)]
    }


    return chatgraph().invoke(state,config=config)


@app.post("/Datadog_Monitor")
async def create_item(alert: DataDogAlert):
    
    initial_state = {
        "raw_input": {
            "Title": alert.event['error']['message'],
            "Body": alert.event['error']['details']
        },
        "source": "DataDog",
        "classification": {
                           "category":"",
                           "sub_category":"",
                           "severity":"",
                           "confidence":""
                           },
        "severity": "",
        "assigned_to": "",
        "next_action": "",
        "extracted_entities" : "",
        "status": "received"
    }    
    return TicketCreatorGraph().run(initial_state)

# @app.post("/Sifflet_Monitor")
# async def create_item(alert: DataDogAlert):
#     print(alert.event)
#     return {
#         "message": "Item created successfully",
#         "data": alert
#     }



    #email_action = intent_classification(email_subject = alert.Subject,email_body=alert.Body)
    return {
        "message": "Email Received successfully",
        "data": initial_state
    }














# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}