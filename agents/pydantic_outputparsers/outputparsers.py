from pydantic import BaseModel, Field
from typing import Optional, List

class Email_Classification(BaseModel):
    category: str = Field(
        description="One of FOLLOW_UP, STANDARD_REQUEST, INCIDENT, CHANGE_REQUEST, ACCESS_REQUEST, QUESTION, APPROVAL_RESPONSE, AUTOMATED_NOTIFICATION, UNKNOWN"
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