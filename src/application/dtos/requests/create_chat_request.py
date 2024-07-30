from pydantic import BaseModel


class CreateChatRequest(BaseModel):
    user_id: str
    friend_id: str
    chat_type: str  # IA o PERSONAL
