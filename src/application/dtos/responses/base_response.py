import json

from pydantic import BaseModel


class BaseResponse(BaseModel):
    data: dict | None
    message: str
    success: bool
    status_code: int
    http_status: str

    # def to_dict(self):
    #     return {
    #         'data': self.data,
    #         'message': self.message,
    #         'success': self.success,
    #         'status_code': self.status_code,
    #         'http_status': self.http_status
    #     }
    #
    # def to_json(self):
    #     return json.dumps(self.to_dict())
