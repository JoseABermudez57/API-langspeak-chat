import uuid

from sqlalchemy import Column, String, Text, DateTime, ForeignKey, UUID

from sqlalchemy.orm import relationship

from database import Base


# Models
class Chat(Base):
    __tablename__ = "chats"
    id = Column(String(36), primary_key=True, default=uuid.uuid4)
    user_id = Column(String(255))
    friend_id = Column(String(255))
    chat_type = Column(String(20))
    messages = relationship("Message", back_populates="chat")


class Message(Base):
    __tablename__ = "messages"
    id = Column(String(36), primary_key=True, default=uuid.uuid4)
    content = Column(String(10000))
    message_type = Column(String(20))
    sender_id = Column(String(255))
    recipient_id = Column(String(255))
    chat_id = Column(String(255), ForeignKey("chats.id"))
    chat = relationship("Chat", back_populates="messages")


class TimeIA(Base):
    __tablename__ = "time_ia"
    id = Column(String(36), primary_key=True, default=uuid.uuid4)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    user_id = Column(String(255))
