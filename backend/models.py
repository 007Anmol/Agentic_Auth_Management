from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str = Field(..., description="The user's input message")
    history: Optional[List[Dict[str, Any]]] = Field(default=[], description="Chat history for context")

class ChatResponse(BaseModel):
    success: bool
    response: str
    error: Optional[str] = None
