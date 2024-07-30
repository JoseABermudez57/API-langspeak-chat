from pydantic import BaseModel


class ChatResponse( BaseModel):
    chat_uuid: str
    friend_uuid: str
    profile_picture: str
    name: str
    last_message: str
    date: str
    time: str
