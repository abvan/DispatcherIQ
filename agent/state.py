from pydantic import BaseModel

class AgentState(BaseModel):
    raw_input: dict | None = None
    parsed: dict | None = None
    category: str | None = None
    engineer: dict | None = None
    ticket_id: str | None = None
    notification_status: str | None = None