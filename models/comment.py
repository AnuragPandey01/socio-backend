from sqlmodel import SQLModel, Field, Relationship
import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import User, Post


class Comment(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    text: str = Field(nullable=False)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    user: "User" = Relationship(back_populates="comments")
    post_id: uuid.UUID = Field(foreign_key="post.id", nullable=False)
    post: "Post" = Relationship(back_populates="comments")
