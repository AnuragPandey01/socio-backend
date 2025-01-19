from pydantic import BaseModel, EmailStr
import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from schema import PostPublic


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    username: str
    bio: str | None
    profile_image: str | None


class UserPublic(UserBase):
    id: uuid.UUID


class UserWithPosts(UserPublic):
    posts: list["PostPublic"]


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    username: str
    password: str
