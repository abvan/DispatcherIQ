from fastapi import FastAPI,Request
from pydantic import BaseModel
from typing import Any

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

##------------------------ POST endpoints(alerts Monitor (Webhooks))----------------------------------##
@app.post("/Datadog_Monitor")
async def create_item(alert: DataDogAlert):
    print(alert.event)
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

# @app.post("/Email_Monitor")
# async def create_item(alert: DataDogAlert):
#     print(alert.event)
#     return {
#         "message": "Item created successfully",
#         "data": alert
#     }

##------------------------ Helper Functions----------------------------------##
def create_ticket():
    # This Function needs to create a service Ticket in Jira/Neops. Temporarily it will save it in an Excel File
    pass

def assign_engineer():
    #This Function will check the availability of the engineers , assess the complexity of the task and assign to the resources.
    pass

def check_updates_and_save():
    #This Function will take the updates of all the open tickets every 1hr and Save the latest updates in the database
    pass

def send_teams_message():
    #This Function will send message to engineer or Operations Teams Group Chat Regarding Ticket Creation and Assignment.
    pass

def send_email():
    #This function will send the emails regarding Updates and acknowledment to the users.
    pass




##------------------------  -----------------------------##













# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}