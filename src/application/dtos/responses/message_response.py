from typing import List

from pydantic import BaseModel


class MessageResponse(BaseModel):
    chat_uuid: str
    messages: List[dict]
