import json

from models import Message
from src.application.dtos.requests.send_message_request import SendMessageRequest
from src.application.dtos.responses.base_response import BaseResponse
from src.application.dtos.responses.get_message_analyzed_response import GetMessageAnalyzedResponse


class SendMessageUseCase:
    def __init__(self, db, message_publisher):
        self.db = db
        self.message_publisher = message_publisher

    def execute(self, request: SendMessageRequest):
        message = {
            "content": request.content,
            "type": request.message_type,
            "user_id": request.sender_id,
            "uuid": request.chat_id
        }
        self.message_publisher.execute(json.dumps(message))
        # request.content = content
        db_message = Message(**request.dict())
        self.db.add(db_message)
        self.db.commit()
        self.db.refresh(db_message)
        return BaseResponse(data=message, status_code=200, message="Message sent successfully", success=False, http_status="OK")
