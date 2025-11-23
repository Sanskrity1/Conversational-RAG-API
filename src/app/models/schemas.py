from pydantic import BaseModel, EmailStr
from typing import Optional, Any, List

class ChatMessage(BaseModel):
    role: str
    text: str

class ChatResponse(BaseModel):
    reply: str
    used_contexts: Optional[List[dict]] = None

class Booking(BaseModel):
    id: str
    name: str
    email: EmailStr
    datetime_iso: str
    notes: Optional[str] = None
    created_at: Optional[str] = None
