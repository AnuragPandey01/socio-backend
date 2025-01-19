from enum import Enum
from sqlmodel import SQLModel, Field
import uuid


class RequestStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class UserFollowMapping(SQLModel, table=True):
    follower_id: uuid.UUID = Field(
        nullable=False, primary_key=True, foreign_key="user.id", ondelete="CASCADE"
    )
    following_id: uuid.UUID = Field(
        nullable=False, primary_key=True, foreign_key="user.id", ondelete="CASCADE"
    )
    status: RequestStatus = Field(default=RequestStatus.PENDING, nullable=False)
