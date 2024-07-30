from enum import Enum


class QueueEnum(Enum):

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

    QUEUE_ANALYZED_MESSAGE_REQUEST = {
        "queue": "analyzed_message_request",
        "exchange": "analysis",
        "routing_key": "message_request.analyzed"
    }

    QUEUE_ANALYZED_MESSAGE_RESPONSE = {
        "queue": "analyzed_message_response",
        "exchange": "analysis",
        "routing_key": "message_response.analyzed"
    }
