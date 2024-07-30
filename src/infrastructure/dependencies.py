import threading
from src.infrastructure.adapters.ports.inputs.controllers.chat_controller import router as router_chat
from src.infrastructure.adapters.ports.inputs.controllers.health_controller import router as router_health
from src.infrastructure.adapters.ports.inputs.consumers.analyze_message_consumer import MessageConsumer
from src.application.dtos.responses.get_message_analyzed_response import GetMessageAnalyzedResponse

response = GetMessageAnalyzedResponse()
message_consumer = MessageConsumer(response)


def init_routers(app):
    app.include_router(router_health, prefix='/health/api')
    app.include_router(router_chat, prefix='/chats/api')


def init_rabbitmq():
    threading.Thread(target=message_consumer.execute).start()
