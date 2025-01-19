from .post import Post
from .user import User
from .comment import Comment
from .post_image_mapping import PostImageMapping
from .user_follow_mapping import UserFollowMapping, RequestStatus
from .chat import Chat
from .post_like_mapping import PostLikeMapping


__all__ = [
    "User",
    "Post",
    "Comment",
    "PostImageMapping",
    "UserFollowMapping",
    "Chat",
    "PostLikeMapping",
    "RequestStatus"
]


for model_name in __all__:
    model = globals().get(model_name)
    if model and hasattr(model, "model_rebuild"):
        model.model_rebuild()
