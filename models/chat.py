from sqlmodel import SQLModel, Field
import uuid
from datetime import datetime

class Chat(SQLModel,table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4,primary_key=True,nullable=False)
    sender_id: uuid.UUID = Field(foreign_key="user.id",nullable=False)
    receiver_id: uuid.UUID = Field(foreign_key="user.id",nullable=False)
    message: str = Field(nullable=False)
    created_at : datetime = Field(default_factory=datetime.utcnow)

class SendMessage(SQLModel):
    receiver_id: uuid.UUID
    message: str
