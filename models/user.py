from sqlmodel import SQLModel,Field, Relationship
from pydantic import EmailStr
from models.post import Post,PostPublic,PostLikeMapping
import uuid
from enum import Enum


class RequestStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class UserFollowMapping(SQLModel,table=True):
    follower_id: uuid.UUID = Field(
        nullable=False,
        primary_key=True,
        foreign_key="user.id",
        ondelete="CASCADE"
    )
    following_id: uuid.UUID = Field(
        nullable=False,
        primary_key=True,
        foreign_key="user.id",
        ondelete="CASCADE"
    )
    status: RequestStatus = Field(default=RequestStatus.PENDING, nullable=False)


class User(SQLModel,table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    email: EmailStr = Field(nullable=False, unique=True)
    username: str = Field(nullable=False, unique=True)
    password: str = Field()
    bio: str = Field(nullable=True)
    profile_image: str = Field(nullable=True)
    posts: list[Post] = Relationship(
        back_populates="user"
    )
    liked_posts: list[Post] = Relationship(
        back_populates="likes",
        link_model=PostLikeMapping
    )


class UserBase(SQLModel):
    first_name: str
    last_name: str
    email: EmailStr
    username: str
    bio: str | None
    profile_image: str | None


class UserPublic(UserBase):
    id: uuid.UUID


class UserWithPosts(UserPublic):
    posts: list[PostPublic]


class UserCreate(UserBase):
    password: str


class UserLogin(SQLModel):
    username: str
    password: str

