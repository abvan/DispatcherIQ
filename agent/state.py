from pydantic import BaseModel
from typing import TypedDict, Optional, List, Dict, Any

class AgentState(BaseModel):
    ticket_id: str | None = None
    raw_input: dict | None = None
    summarised_input: str | None = None
    category: str | None = None
    sub_catergory : str | None = None
    severity : int | None = None
    engineer : dict | None = None
    
    notification_status: str | None = None


class EmailAgentState(TypedDict, total=False):
    # Raw input
    email_subject: str
    email_body: str
    thread_id: Optional[str]
    mail_chain_depth: Optional[int]

    # Classification results
    classification: Dict[str, Any]
    thread_context: Dict[str, Any]
    signals: List[str]
    recommended_next_action: str

    # Execution metadata
    status: str
    errors: List[str]