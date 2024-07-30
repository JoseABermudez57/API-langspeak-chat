from models import Chat
from src.application.dtos.requests.create_chat_request import CreateChatRequest
from src.application.dtos.responses.base_response import BaseResponse


class CreateChatUseCase:
    def __init__(self, db):
        self.db = db

    def execute(self, request: CreateChatRequest):

        # chat_id = request.user_id + "-" + request.friend_id
        db_chat = Chat(**request.dict())
        self.db.add(db_chat)
        self.db.commit()
        self.db.refresh(db_chat)
        chat = {
            "id": db_chat.id,
            "user_id": db_chat.user_id,
            "friend_id": db_chat.friend_id,
            "chat_type": db_chat.chat_type
        }
        return BaseResponse(data=chat, status_code=201, message="Chat created successfully", success=True,
                            http_status="CREATED")
