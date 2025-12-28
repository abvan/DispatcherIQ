from pydantic import BaseModel
from typing import TypedDict, Optional, List, Dict, Any
from ..parsing_models import Classification

class input_structure(BaseModel):
    Title : str
    Body : str

class DispatcherState(TypedDict):
    ticket_id: Optional[str]
    raw_input: input_structure
    classification: Classification 
    assigned_to: Optional[str]
    summary: Optional[str]
    next_action: Optional[str]
    extracted_entities: Optional[dict]
    response_message: Optional[str]
    status: str # Aknowledged | Ticket Created | Engineer Assigned | InProgress | Completed |
    lastUpdateTime: str
    