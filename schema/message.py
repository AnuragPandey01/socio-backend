from pydantic import BaseModel
import uuid


class SendMessage(BaseModel):
    receiver_id: uuid.UUID
    message: str
