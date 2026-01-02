from pydantic import BaseModel
from typing import TypedDict, Optional, List, Dict, Any
from ..parsing_models import Classification


class input_structure(BaseModel) :
    Title : str
    Body : str

class TicektCreatorState(TypedDict) :
    ticket_id: Optional[str]
    raw_input: input_structure
    source: Optional[str] # email | alert(datadog,sifflet etc)
    classification: Classification 
    assigned_to: Optional[str]
    summary: Optional[str]
    status:str  # Ticket Created | Require More Info
    lastUpdateTime: str