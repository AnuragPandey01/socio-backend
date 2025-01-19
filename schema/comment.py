from pydantic import BaseModel
import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from schema import UserPublic


class CommentWithUser(BaseModel):
    id: uuid.UUID
    text: str
    user: "UserPublic"
    post_id: uuid.UUID
