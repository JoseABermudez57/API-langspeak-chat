from src.infrastructure.configurations.rabbit_mq_config import setup_rabbitmq
from src.infrastructure.enums.queues_enums import QueueEnum


class MessagePublisher:

    def __init__(self, ):
        self.queue_name = QueueEnum.QUEUE_ANALYZED_MESSAGE_REQUEST.value["queue"]
        self.exchange_name = QueueEnum.QUEUE_ANALYZED_MESSAGE_REQUEST.value["exchange"]
        self.routing_key = QueueEnum.QUEUE_ANALYZED_MESSAGE_REQUEST.value["routing_key"]

    def execute(self, message_analyzed):
        try:
            channel = setup_rabbitmq(self.queue_name, self.exchange_name, self.routing_key)
            channel.basic_publish(routing_key=self.routing_key,
                                  exchange=self.exchange_name,
                                  body=message_analyzed)
        except Exception as e:
            print(f'Error while publishing message, Analyze Message queue: {str(e)}')
