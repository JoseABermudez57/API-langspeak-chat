from models import TimeIA
from src.application.dtos.requests.time_ia_request import TimeIARequest
from src.application.dtos.responses.base_response import BaseResponse


class SendTimeChatUseCase:
    def __init__(self, db):
        self.db = db

    def execute(self, request: TimeIARequest):
        try:
            db_time_ia = TimeIA(**request.dict())
            self.db.add(db_time_ia)
            self.db.commit()
            self.db.refresh(db_time_ia)
            return BaseResponse(data=db_time_ia, status_code=200, message="Time registered successfully", success=True, http_status="OK")
        except Exception as e:
            return BaseResponse(status_code=500, message=str(e), success=False, http_status="Internal Server Error")
