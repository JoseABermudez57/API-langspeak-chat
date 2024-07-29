import uvicorn
from datetime import datetime
from typing import List, Optional, Annotated

from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Chat, Message, TimeIA


class TextInput(BaseModel):
    text: str


class AnalysisResult(BaseModel):
    original_text: str
    filtered_text: str
    sentiment: str
    score: float


app = FastAPI()


# DTOs
class CreateChatRequest(BaseModel):
    user_id: str
    friend_id: str
    chat_type: str  # IA o PERSONAL


class SendMessageRequest(BaseModel):
    content: Optional[str] = None
    message_type: str  # AUDIO o TEXT
    sender_id: str
    recipient_id: str  # uuid o "IA"
    chat_id: str


class TimeIARequest(BaseModel):
    start_time: datetime
    end_time: datetime
    user_id: str


class ChatResponse(BaseModel):
    chat_uuid: str
    friend_uuid: str
    profile_picture: str
    name: str
    last_message: str
    date: str
    time: str


class MessageResponse(BaseModel):
    chat_uuid: str
    messages: List[dict]


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


# Health check
@app.get("/health")
async def health():
    return {"status": "Ok"}


# Endpoints
@app.post("/chats/api/v1/create", status_code=status.HTTP_201_CREATED)
async def create_chat(request: CreateChatRequest, db: db_dependency):
    chat_id = request.user_id + "-" + request.friend_id
    db_chat = Chat(id=chat_id, **request.dict())
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return {"status": "Chat created", "data": request.dict()}


@app.post("/chats/api/v1/send-message", status_code=status.HTTP_200_OK)
async def send_message(request: SendMessageRequest,
                       # audio: Optional[UploadFile] = File(None),
                       db: Session = Depends(get_db)):

    db_message = Message(**request.dict())
    # db_message.content = request.content
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return {"status": "Message sent", "data": request.dict()}


@app.post("/chats/api/v1/time-ia", status_code=status.HTTP_200_OK)
async def time_ia(request: TimeIARequest, db: db_dependency):
    db_time_ia = TimeIA(**request.dict())
    db.add(db_time_ia)
    db.commit()
    db.refresh(db_time_ia)
    return {"status": "Time registered", "data": request.dict()}


@app.get("/chats/api/v1/graphic/{user_uuid}", status_code=status.HTTP_200_OK)
async def get_graphic(user_uuid: str):
    # Logic to get graphic data
    return {
        "user_uuid": user_uuid,
        "list_data_user": [
            {"date": "2024-07-23", "seconds": 900},
            {"date": "2024-06-23", "seconds": 500},
            {"date": "2024-05-23", "seconds": 200},
        ]
    }


@app.get("/chats/api/v1/user-chats/{user_uuid}", status_code=status.HTTP_200_OK)
async def get_user_chats(user_uuid: str, db: db_dependency):
    chats = db.query(Chat).filter(Chat.user_id == user_uuid).all()
    if not chats:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chats not found")
    return {
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


@app.get("/chats/api/v1/message/{chat_uuid}", status_code=status.HTTP_200_OK)
async def get_message(chat_uuid: str, db: db_dependency):
    messages = db.query(Message).filter(Message.chat_id == chat_uuid).all()
    if not messages:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Messages not found")
    return MessageResponse(
        chat_uuid=chat_uuid,
        messages=[
            {
                "message_uuid": message.id,
                "type": message.message_type,
                "sender_id": message.sender_id,
                "recipient_id": message.recipient_id,
                "content": message.content,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "time": datetime.now().strftime("%H:%M:%S")
            } for message in messages
        ]
    )


def main():
    # uvicorn.run(app, host="0.0.0.0", port=8082)
    uvicorn.run("main:app", host="localhost", port=8083, reload=True)


if __name__ == "__main__":
    main()
