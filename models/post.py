from sqlmodel import SQLModel, Field, Relationship
import uuid
#from datetime import UTC

class PostLikeMapping(SQLModel,table=True):
    post_id: uuid.UUID = Field(nullable=False,primary_key=True,foreign_key="post.id",ondelete="CASCADE")
    user_id: uuid.UUID = Field(nullable=False,primary_key=True,foreign_key="user.id",ondelete="CASCADE")

class Post(SQLModel,table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4,primary_key=True,nullable=False)
    text: str
    images: list["PostImageMapping"] = Relationship(back_populates="post",cascade_delete=True)
    user_id: uuid.UUID = Field(nullable=False,foreign_key="user.id",ondelete="CASCADE")
    user: "User" = Relationship(back_populates="posts")
    #created_at = Field(default_factory=datetime.utcnow, nullable=False)

    likes: list["User"] = Relationship(back_populates="liked_posts",cascade_delete=True,link_model=PostLikeMapping)

class PostCreate(SQLModel):
    text: str

class PostPublic(PostCreate):
    id: uuid.UUID
    images: list["PostImageMapping"]

class PostImageMapping(SQLModel,table=True):
    post_id: uuid.UUID = Field(nullable=False,primary_key=True,foreign_key="post.id",ondelete="CASCADE")
    post: "Post" = Relationship(back_populates="images")
    image_url: str = Field(nullable=False,primary_key=True)





