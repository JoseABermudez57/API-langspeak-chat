from abc import ABC, abstractmethod

from src.application.dtos.responses.base_response import BaseResponse


class IChatServicePortInput(ABC):

    @abstractmethod
    def send_message(self, message: str) -> BaseResponse:
        pass

    @abstractmethod
    def create_chat(self, message: str) -> BaseResponse:
        pass

    @abstractmethod
    def time_ia(self, message: str) -> BaseResponse:
        pass

    @abstractmethod
    def get_graphic(self, message: str) -> BaseResponse:
        pass

    @abstractmethod
    def get_user_chats(self, message: str) -> BaseResponse:
        pass

    @abstractmethod
    def get_messages(self, message: str) -> BaseResponse:
        pass
