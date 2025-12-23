from pydantic import BaseModel
from typing import TypedDict, Optional, List, Dict, Any
from .parsing_models import Classification

class input_structure(BaseModel):
    Title : str
    Body : str

class DispatcherState(TypedDict):
    ticket_id: Optional[str]
    raw_input: input_structure
    source: Optional[str] # email | alert(datadog,sifflet etc) | stakeholder
    classification: Classification 
    severity: Optional[str]
    assigned_to: Optional[str]
    next_action: Optional[str]
    extracted_entities: Optional[dict]
    response_message: Optional[str]
    status: str # Aknowledged | Ticket Created | Engineer Assigned | InProgress | Completed |

# raw_input = input_structure(
#     Title="Issues in PowerBI report",
#     Body="Hello operations team , the gross sales margin in the consolidated sales report are not correct when i compare it with the SAP system, could you please check on this ASAP. This is quiet urgent since the Director needs the sales figure in this closing period."
# )

# state_object = DispatcherState(
#     raw_input = raw_input,
#     source = 'Email'
# )

# print(state_object['raw_input'].Title)