import uuid
from sqlmodel import SQLModel, Field


class PostLikeMapping(SQLModel, table=True):
    post_id: uuid.UUID = Field(
        nullable=False, primary_key=True, foreign_key="post.id", ondelete="CASCADE"
    )
    user_id: uuid.UUID = Field(
        nullable=False, primary_key=True, foreign_key="user.id", ondelete="CASCADE"
    )
