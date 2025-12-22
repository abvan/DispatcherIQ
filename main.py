from fastapi import FastAPI,Request
from pydantic import BaseModel
from typing import Any

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import asynccontextmanager
from datetime import datetime

# from agent.tools import classify_email
# from agent.workflow_tools import intent_classification
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
class Item(BaseModel):
    name: str
    price: float
    in_stock: bool = False
    latest : str

#class tagsDetails(BaseModel):

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


##------------------------ POST endpoints(alerts Monitor (Webhooks))----------------------------------##
@app.post("/Datadog_Monitor")
async def create_item(alert: DataDogAlert):
    print(alert.event['error']['message'])
    return {
        "message": "Item created successfully",
        "data": alert
    }

# @app.post("/Sifflet_Monitor")
# async def create_item(alert: DataDogAlert):
#     print(alert.event)
#     return {
#         "message": "Item created successfully",
#         "data": alert
#     }

@app.post("/Email_Monitor")
async def create_item(alert: EmailAlert):
    
    initial_state = {
        "raw_input": {
            "Title": alert.Subject,
            "Body": alert.Body
        },
        "source": "Email",
        "classification": None,
        "severity": None,
        "assigned_to": None,
        "next_action":None,
        "extracted_entities" : None,
        "status": "received"
    }

    return dispatcher_graph.invoke(initial_state)

    #email_action = intent_classification(email_subject = alert.Subject,email_body=alert.Body)
    return {
        "message": "Email Received successfully",
        "data": initial_state
    }














# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}