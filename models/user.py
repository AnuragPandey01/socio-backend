from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr
import uuid
from models.post_like_mapping import PostLikeMapping
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import PostLikeMapping, Post, Comment


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    email: EmailStr = Field(nullable=False, unique=True)
    username: str = Field(nullable=False, unique=True, index=True)
    password: str = Field()
    bio: str = Field(nullable=True)
    profile_image: str = Field(nullable=True)
    posts: list["Post"] = Relationship(back_populates="user")
    liked_posts: list["Post"] = Relationship(
        back_populates="likes", link_model=PostLikeMapping
    )
    comments: list["Comment"] = Relationship(back_populates="user")
