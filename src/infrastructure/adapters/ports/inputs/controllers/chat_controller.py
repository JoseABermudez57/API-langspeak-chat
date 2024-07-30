import httpx
from fastapi import APIRouter, HTTPException, responses, Depends, status

from src.application.dtos.requests.create_chat_request import CreateChatRequest
from src.application.dtos.requests.send_message_request import SendMessageRequest
from src.application.dtos.requests.time_ia_request import TimeIARequest
from src.application.services.chat_service import ChatService

from sqlalchemy.orm import Session
from database import SessionLocal
# from typing import Annotated

from src.application.services.use_cases.create_chat_use_case import CreateChatUseCase
from src.application.services.use_cases.get_graphic_use_case import GetGraphicUseCase
from src.application.services.use_cases.send_message_use_case import SendMessageUseCase
from src.application.services.use_cases.get_all_chats_use_case import GetAllChatsUseCase
from src.application.services.use_cases.send_time_chat_use_case import SendTimeChatUseCase
from src.application.services.use_cases.get_all_message_by_chat_use_case import GetAllMessageByChatUseCase
from src.infrastructure.adapters.ports.outputs.publishers.analyzer_message_publisher import MessagePublisher
from src.infrastructure.adapters.ports.inputs.consumers.analyze_message_consumer import MessageConsumer

message_consumer = MessageConsumer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# db_dependency = Annotated[Session, Depends(get_db)]

message_publisher = MessagePublisher()


def get_send_message_use_case(db: Session = Depends(get_db)):
    return SendMessageUseCase(db)


def get_create_chat_use_case(db: Session = Depends(get_db)):
    return CreateChatUseCase(db)


def get_send_time_chat_use_case(db: Session = Depends(get_db)):
    return SendTimeChatUseCase(db)


def get_get_graphic_use_case(db: Session = Depends(get_db)):
    return GetGraphicUseCase(db)


def get_get_all_chats_use_case(db: Session = Depends(get_db)):
    return GetAllChatsUseCase(db)


def get_get_all_message_by_chat_use_case(db: Session = Depends(get_db)):
    return GetAllMessageByChatUseCase(db)


# sendMessageUseCase = SendMessageUseCase(db_dependency, message_publisher)
# createChatUseCase = CreateChatUseCase(db_dependency)
# sendTimeChatUseCase = SendTimeChatUseCase(db_dependency)
# getGraphicUseCase = GetGraphicUseCase(db_dependency)
# getAllChatsUseCase = GetAllChatsUseCase(db_dependency)
# getAllMessageByChatUseCase = GetAllMessageByChatUseCase(db_dependency)

# chat_service = ChatService(sendMessageUseCase, createChatUseCase, sendTimeChatUseCase,
#                            getGraphicUseCase, getAllChatsUseCase, getAllMessageByChatUseCase)

def get_chat_service(
        send_message_use_case: SendMessageUseCase = Depends(get_send_message_use_case),
        create_chat_use_case: CreateChatUseCase = Depends(get_create_chat_use_case),
        send_time_chat_use_case: SendTimeChatUseCase = Depends(get_send_time_chat_use_case),
        get_graphic_use_case: GetGraphicUseCase = Depends(get_get_graphic_use_case),
        get_all_chats_use_case: GetAllChatsUseCase = Depends(get_get_all_chats_use_case),
        get_all_message_by_chat_use_case: GetAllMessageByChatUseCase = Depends(get_get_all_message_by_chat_use_case)):
    return ChatService(
        send_message_use_case,
        create_chat_use_case,
        send_time_chat_use_case,
        get_graphic_use_case,
        get_all_chats_use_case,
        get_all_message_by_chat_use_case
    )


router = APIRouter()


# Endpoints
@router.post("/v1/create", status_code=status.HTTP_201_CREATED)
async def create_chat(request: CreateChatRequest, chat_service: ChatService = Depends(get_chat_service)):
    return chat_service.create_chat(request)


@router.post("/v1/send-message", status_code=status.HTTP_200_OK)
async def send_message(request: SendMessageRequest, chat_service: ChatService = Depends(get_chat_service)
                       # audio: Optional[UploadFile] = File(None),
                       ):
    message = {
        "content": request.content,
        "type": request.message_type,
        "user_id": request.sender_id,
        "uuid": request.chat_id
    }
    async with httpx.AsyncClient() as client:
        response = await client.post('http://3.225.80.186:8087/analysis/api/v1/analyzer', json=message)
        json = response.json()
        if response.status_code == 200:
            content_analyzed = json['data']['content']
            request.content = content_analyzed
    return chat_service.send_message(request)


@router.post("/v1/time-ia", status_code=status.HTTP_200_OK)
async def time_ia(request: TimeIARequest, chat_service: ChatService = Depends(get_chat_service)):
    return chat_service.time_ia(request)


@router.get("/v1/graphic/{user_uuid}", status_code=status.HTTP_200_OK)
async def get_graphic(user_uuid: str, chat_service: ChatService = Depends(get_chat_service)):
    return chat_service.get_graphic(user_uuid)


@router.get("/v1/user-chats/{user_uuid}", status_code=status.HTTP_200_OK)
async def get_user_chats(user_uuid: str, chat_service: ChatService = Depends(get_chat_service)):
    return chat_service.get_user_chats(user_uuid)


@router.get("/v1/message/{chat_uuid}", status_code=status.HTTP_200_OK)
async def get_message(chat_uuid: str, chat_service: ChatService = Depends(get_chat_service)):
    return chat_service.get_messages(chat_uuid)
