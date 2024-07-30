import json

from src.infrastructure.enums.queues_enums import QueueEnum
from src.infrastructure.configurations.rabbit_mq_config import setup_rabbitmq


class MessageConsumer:
    def __init__(self):
        self.queue_name = QueueEnum.QUEUE_ANALYZE_MESSAGE_RESPONSE.value["queue"]
        self.exchange_name = QueueEnum.QUEUE_ANALYZE_MESSAGE_RESPONSE.value["exchange"]
        self.routing_key = QueueEnum.QUEUE_ANALYZE_MESSAGE_RESPONSE.value["routing_key"]

    def execute(self):
        try:
            channel = setup_rabbitmq(self.queue_name, self.exchange_name, self.routing_key)
            channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback, auto_ack=True)
            channel.start_consuming()
        except Exception as e:
            print(f'Error while consuming message, Analyze Message queue: {str(e)}')

    def callback(self, ch, method, properties, body):
        request = json.loads(body)
        content = request['data']['content']
        print(content)
