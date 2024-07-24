import uvicorn
from datetime import datetime
from typing import List, Optional, Annotated

from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Chat, Message, TimeIA
from transformers import pipeline
import re
from nltk.tokenize import word_tokenize
import nltk
from better_profanity import Profanity

nltk.download('punkt', quiet=True)


model_multilingual = "nlptown/bert-base-multilingual-uncased-sentiment"
analytic_sentiments_multilingual = pipeline("sentiment-analysis", model=model_multilingual)

profanity_list = ['puto', 'idiot', 'fuck', "Mamon", "Pinche", "verga", "huevon", "Chinga", "Pendejo", "Chingar", "Puta",
                  "huevos", "Chachalaco", "Malacopa", "Chingaquedito", "Argüendero", "chingada", "Cascado", "asshole",
                  "hooker", "Dumbass", "Motherfucker", "bitch", "perra", "Imbecil", "estupido", "maricon", "mierda",
                  "maldito", "pene", "p3n3", "pito", "p1t0", "pit0", "p1to", "bastard", "bastardo", "putas", "putos",
                  "dick", "d1ck", "fucking", "fuck1ng", "fock", "f0ck", "vtm", "ptm", "pt" "chtm", "ctm", "vrg"]

profanity = Profanity()
profanity.add_censor_words(profanity_list)


class TextInput(BaseModel):
    text: str


class AnalysisResult(BaseModel):
    original_text: str
    filtered_text: str
    sentiment: str
    score: float


def clean_text(text: str) -> str:
    contractions = {
        "I'm": "I am",
        "you're": "you are",
        "he's": "he is",
        "she's": "she is",
        "it's": "it is",
        "we're": "we are",
        "they're": "they are",
        "I've": "I have",
        "you've": "you have",
        "we've": "we have",
        "they've": "they have",
        "isn't": "is not",
        "aren't": "are not",
        "wasn't": "was not",
        "weren't": "were not",
        "won't": "will not",
        "wouldn't": "would not",
        "don't": "do not",
        "doesn't": "does not",
        "didn't": "did not",
        "can't": "cannot",
        "couldn't": "could not",
        "shouldn't": "should not",
        "mightn't": "might not",
        "mustn't": "must not"
    }
    text = text.lower()
    for contraction, full_form in contractions.items():
        text = text.replace(contraction.lower(), full_form.lower())
    text = re.sub(r'[^a-zA-Záéíóúüñ\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def analyze_and_filter(text: str) -> tuple:
    text = clean_text(text)
    result = analytic_sentiments_multilingual(text)

    sentiment = result[0]['label']
    score = result[0]['score']
    # tokens = word_tokenize(text)

    if sentiment in ['1 star', '2 stars'] or (sentiment in ['4 stars', '5 stars'] and score < 0.8):
        filtered_text = profanity.censor(text=text, censor_char="*")
    else:
        filtered_text = text

    return filtered_text, sentiment, score

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
    content = request.content
    sentiment = None
    score = None
    #
    if request.message_type == "TEXT":
        content, sentiment, score = analyze_and_filter(content)

    print(f"Sentiment: {sentiment}, Score: {score}")

    db_message = Message(**request.dict(), content=content)
    # db_message = Message(**request.dict())
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
