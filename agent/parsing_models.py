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

class AlertIncidentSummary(BaseModel):
    summary: str = Field(
        description="Concise summary of the alert and its impact (max 50 words)."
    )
    root_cause_explanation: str = Field(
        description="Reasoned explanation of why the failure occurred (max 50 words)."
    )
    possible_solutions: List[str] = Field(
        description="Actionable possible solutions or fixes (each item concise, overall max 50 words)."
    )
    next_recommended_actions: List[str] = Field(
        description="Immediate next steps for support engineers (each item concise, overall max 50 words)."
    )
