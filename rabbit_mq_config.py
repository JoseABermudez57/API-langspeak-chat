import pika
import os
from dotenv import load_dotenv
# import ssl
#
#
# ssl_context = ssl.create_default_context()
# ssl_context.check_hostname = False
# ssl_context.verify_mode = ssl.CERT_NONE
# ssl_options=pika.SSLOptions(ssl_context)

load_dotenv()
hostname = os.getenv('RABBITMQ_HOST')
protocol = os.getenv('RABBITMQ_PROTOCOL')
user = os.getenv('RABBITMQ_USER')
password = os.getenv('RABBITMQ_PASS')
port = os.getenv('RABBITMQ_PORT')


def setup_rabbitmq(queue_name, exchange_name, routing_key):
    credentials = pika.PlainCredentials(user, password)
    parameters = pika.ConnectionParameters(hostname, int(port), '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange_name, exchange_type='direct', durable=True)
    channel.queue_declare(queue=queue_name, durable=True)
    channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)
    return channel
