from enum import Enum


class Queue(Enum):

    QUEUE_ANALYZE_MESSAGE_REQUEST = {
        "queue": "analyze_message_request",
        "exchange": "analysis",
        "routing_key": "message_request.analyze"
    }

    QUEUE_ANALYZE_MESSAGE_RESPONSE = {
        "queue": "analyze_message_response",
        "exchange": "analysis",
        "routing_key": "message_response.analyze"
    }
