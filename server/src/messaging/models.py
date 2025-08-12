from datetime import datetime
from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field

class MessageType(str, Enum):
    TEXT = "text"
    FILE = "file"
    AUDIO = "audio"

class Message(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    content: str
    message_type: MessageType
    file_url: Optional[str] = None
    file_name: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_read: bool = False

    class Config:
        from_attributes = True

class ChatRoom(BaseModel):
    id: int
    user1_id: int
    user2_id: int
    last_message_id: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True

class UserOnlineStatus(BaseModel):
    user_id: int
    is_online: bool
    last_seen: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True 