"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class MessageSchema(BaseModel):
    """Schema for a message in the conversation"""
    role: str = Field(..., description="Message role: 'user', 'assistant', 'system'")
    content: str = Field(..., description="Message content")


class AgentRequest(BaseModel):
    """Schema for agent request"""
    query: str = Field(..., description="User query or input")
    conversation_history: Optional[List[MessageSchema]] = Field(
        default=None, 
        description="Optional conversation history"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional metadata for the request"
    )


class AgentResponse(BaseModel):
    """Schema for agent response"""
    response: str = Field(..., description="Agent response")
    reasoning: Optional[str] = Field(
        default=None,
        description="Agent's reasoning or thoughts"
    )
    tools_used: Optional[List[str]] = Field(
        default=None,
        description="List of tools used in this response"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional metadata"
    )
