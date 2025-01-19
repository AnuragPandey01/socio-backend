from .user import UserCreate, UserLogin, UserPublic, UserWithPosts
from .post import PostCreate, PostPublic
from .comment import CommentWithUser
from .message import SendMessage

__all__ = [
    "UserCreate",
    "UserLogin",
    "UserPublic",
    "UserWithPosts",
    "PostCreate",
    "PostPublic",
    "CommentWithUser",
    "SendMessage"
]

for model_name in __all__:
    model = globals().get(model_name)
    if model and hasattr(model, "model_rebuild"):
        model.model_rebuild()
