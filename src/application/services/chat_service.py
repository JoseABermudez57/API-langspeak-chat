from src.application.dtos.requests.create_chat_request import CreateChatRequest
from src.application.dtos.requests.send_message_request import SendMessageRequest
from src.application.dtos.requests.time_ia_request import TimeIARequest
from src.application.ports.inputs.i_chat_service_port_input import IChatServicePortInput


class ChatService(IChatServicePortInput):

    def __init__(self, sendMessageUseCase, createChatUseCase, sendTimeChatUseCase,
                           getGraphicUseCase, getAllChatsUseCase, getAllMessageByChatUseCase):
        self.sendMessageUseCase = sendMessageUseCase
        self.createChatUseCase = createChatUseCase
        self.sendTimeChatUseCase = sendTimeChatUseCase
        self.getGraphicUseCase = getGraphicUseCase
        self.getAllChatsUseCase = getAllChatsUseCase
        self.getAllMessageByChatUseCase = getAllMessageByChatUseCase

    def send_message(self, request: SendMessageRequest):
        execute = self.sendMessageUseCase.execute(request)
        return execute

    def create_chat(self, request: CreateChatRequest):
        execute = self.createChatUseCase.execute(request)
        return execute

    def time_ia(self, request: TimeIARequest):
        execute = self.sendTimeChatUseCase.execute(request)
        return execute

    def get_graphic(self, user_uuid: str):
        execute = self.getGraphicUseCase.execute(user_uuid)
        return execute

    def get_user_chats(self, user_uuid: str):
        execute = self.getAllChatsUseCase.execute(user_uuid)
        return execute

    def get_messages(self, chat_uuid: str):
        execute = self.getAllMessageByChatUseCase.execute(chat_uuid)
        return execute
