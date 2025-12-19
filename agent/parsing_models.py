from pydantic import BaseModel, Field
from typing import Optional, List

class Classification(BaseModel):
        category: str = Field(
            description="One of FOLLOW_UP, STANDARD_REQUEST, INCIDENT_ANOMALY, CHANGE_REQUEST, ACCESS_REQUEST, QUESTION, APPROVAL_RESPONSE, AUTOMATED_NOTIFICATION, UNKNOWN"
        )
        sub_category: Optional[str] = Field(
            default=None,
            description="Optional finer classification"
        )
        severity: Optional[str] = Field(
            default=None,
            description="P1, P2, P3 if incident"
        )
        confidence: float = Field(
            description="Confidence between 0 and 1"
        )

class ThreadContext(BaseModel):
    is_reply: bool
    previous_ticket_id: Optional[str] = None
    mail_chain_depth: Optional[int] = None

class ClassifyEmailOutput(BaseModel):
    status: str
    classification: Classification
    thread_context: ThreadContext
    recommended_next_action: str
