import uuid
from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel
from models.post_like_mapping import PostLikeMapping

if TYPE_CHECKING:
    from models import PostImageMapping, User, Comment


class Post(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    text: str
    images: list["PostImageMapping"] = Relationship(
        back_populates="post", cascade_delete=True
    )
    user_id: uuid.UUID = Field(
        nullable=False, foreign_key="user.id", ondelete="CASCADE"
    )
    user: "User" = Relationship(back_populates="posts")

    likes: list["User"] = Relationship(
        back_populates="liked_posts", link_model=PostLikeMapping
    )

    comments: list["Comment"] = Relationship(back_populates="post")
