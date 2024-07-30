from datetime import datetime

from fastapi import HTTPException, status

from models import Message
from src.application.dtos.responses.base_response import BaseResponse
from src.application.dtos.responses.message_response import MessageResponse


class GetAllMessageByChatUseCase:
    def __init__(self, db):
        self.db = db

    def execute(self, chat_uuid: str):
        messages = self.db.query(Message).filter(Message.chat_id == chat_uuid).all()
        if not messages:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Messages not found")
        response = MessageResponse(chat_uuid=chat_uuid, messages=[
            {"message_uuid": message.id, "type": message.message_type, "sender_id": message.sender_id,
             "recipient_id": message.recipient_id, "content": message.content,
             "date": datetime.now().strftime("%Y-%m-%d"), "time": datetime.now().strftime("%H:%M:%S")} for message in
            messages])
        return BaseResponse(data=response, status_code=200, message="Messages found successfully", success=True, http_status="OK")
