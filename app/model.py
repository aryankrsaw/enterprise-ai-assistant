from pydantic import BaseModel
from typing import Any

class ChatRequest(BaseModel):
    message: str
    conversation_id: str

class ChatResponse(BaseModel):
    response: Any