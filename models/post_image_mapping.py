from sqlmodel import SQLModel, Field, Relationship
import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Post

class PostImageMapping(SQLModel, table=True):
    post_id: uuid.UUID = Field(
        nullable=False, primary_key=True, foreign_key="post.id", ondelete="CASCADE"
    )
    post: "Post" = Relationship(back_populates="images")
    image_url: str = Field(nullable=False, primary_key=True)
