
from models import Message
from src.application.dtos.requests.send_message_request import SendMessageRequest
from src.application.dtos.responses.base_response import BaseResponse


class SendMessageUseCase:
    def __init__(self, db):
        self.db = db

    def execute(self, request: SendMessageRequest):
        # message = {
        #     "content": request.content,
        #     "type": request.message_type,
        #     "user_id": request.sender_id,
        #     "uuid": request.chat_id
        # }
        # self.message_publisher.execute(json.dumps(message))
        # # Actualizar el request.content por el content del consumer
        db_message = Message(**request.dict())
        message = {
            "content": db_message.content,
            "message_type": db_message.message_type,
            "sender_id": db_message.sender_id,
            "recipient_id": db_message.recipient_id
        }
        self.db.add(db_message)
        self.db.commit()
        self.db.refresh(db_message)
        return BaseResponse(data=message, status_code=200, message="Message sent successfully", success=False, http_status="OK")
