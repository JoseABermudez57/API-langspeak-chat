from typing import Optional

from pydantic import BaseModel


class SendMessageRequest(BaseModel):
    content: Optional[str] = None
    message_type: str  # AUDIO o TEXT
    sender_id: str
    recipient_id: str  # uuid o "IA"
    chat_id: str
