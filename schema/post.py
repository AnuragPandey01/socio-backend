from pydantic import BaseModel
import uuid


class PostCreate(BaseModel):
    text: str

class PostImage(BaseModel):
    post_id: uuid.UUID
    image_url: str


class PostPublic(PostCreate):
    id: uuid.UUID
    images: list[PostImage]
