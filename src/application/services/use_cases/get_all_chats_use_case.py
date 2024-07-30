from fastapi import HTTPException, status

from models import Chat
from src.application.dtos.responses.base_response import BaseResponse
from src.application.dtos.responses.chat_response import ChatResponse


class GetAllChatsUseCase:
    def __init__(self, db):
        self.db = db

    def execute(self, user_uuid: str):
        chats = self.db.query(Chat).filter(Chat.user_id == user_uuid).all()
        if not chats:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chats not found")
        chats_ = {
            "user_uuid": user_uuid,
            "chats": [
                ChatResponse(
                    chat_uuid=chat.id,
                    friend_uuid=chat.friend_id,
                    profile_picture="http://...",
                    name="Alan",
                    last_message="Hello",
                    date="2024-07-23",
                    time="23:50"
                ) for chat in chats
            ]
        }
        return BaseResponse(data=chats_, status_code=200, message="Chats found successfully", success=True, http_status="OK")
