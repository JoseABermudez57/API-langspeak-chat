from datetime import datetime

from pydantic import BaseModel


class TimeIARequest(BaseModel):
    start_time: datetime
    end_time: datetime
    user_id: str
