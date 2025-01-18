from fastapi import APIRouter, HTTPException, WebSocket, status, Query
from sqlalchemy import and_, exc, or_
from sqlmodel import select
from database import SessionDep
from models.chat import (
    Chat,
    SendMessage
)
from models.user import (
    User,
    UserCreate,
    UserLogin,
    UserPublic,
    UserWithPosts,
    UserFollowMapping,
    RequestStatus
)
from security import (
    Token,
    UserDep,
    create_token,
    hash_password,
    verify_password,
    verify_token,
)
from services.connection_manager import connection_manager


router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register_user(userCreate: UserCreate, session: SessionDep):
    try:
        new_user = User(
            first_name=userCreate.first_name,
            last_name=userCreate.last_name,
            email=userCreate.email,
            username=userCreate.username.lower(),
            password=hash_password(userCreate.password),
            bio=userCreate.bio,
            profile_image=userCreate.profile_image,
        )
        session.add(new_user)
        session.commit()
    except exc.IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="User already exists")
    except Exception as e:
        session.rollback()
        raise e
    return Token(access_token=create_token(str(new_user.id)))


@router.post("/login", response_model=Token)
def login_user(userLogin: UserLogin, session: SessionDep):
    user = session.exec(select(User).where(User.username == userLogin.username)).first()
    if not user or not verify_password(userLogin.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User does not exist"
        )
    return Token(access_token=create_token(str(user.id)))


@router.get("/profile/me", response_model=UserWithPosts)
def get_profile(user: UserDep):
    return user


@router.post("/{user_id}/follow", status_code=status.HTTP_201_CREATED)
def follow_user(user_id: str, user: UserDep, session: SessionDep):
    user_to_follow = session.get(User, user_id)
    if not user_to_follow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    follow_request = UserFollowMapping(follower_id=user.id, following_id=user_id)
    session.add(follow_request)
    session.commit()


@router.post("/{user_id}/accept")
def accept_follow_request(user_id: str, user: UserDep, session: SessionDep):
    follow_request = session.get(
        UserFollowMapping, {"follower_id": user_id, "following_id": user.id}
    )
    if not follow_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Follow request not found"
        )
    follow_request.status = RequestStatus.ACCEPTED
    session.commit()


@router.post("/{user_id}/reject")
def reject_follow_request(user_id: str, user: UserDep, session: SessionDep):
    follow_request = session.get(
        UserFollowMapping, {"follower_id": user_id, "following_id": user.id}
    )
    if not follow_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Follow request not found"
        )
    follow_request.status = RequestStatus.REJECTED
    session.commit()


@router.get("/{user_id}/followers", response_model=list[UserPublic])
def get_followers(
    user_id: str,
    user: UserDep,
    session: SessionDep,
    limit:int=Query(10,ge=1,le=100),
    page:int=Query(1,ge=1)
):
    user_to_get = session.get(User, user_id)
    if not user_to_get:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if user_id != str(user.id):
        authorized = session.exec(
            select(UserFollowMapping).where(
                and_(
                    UserFollowMapping.following_id == user_id,
                    UserFollowMapping.follower_id == user.id,
                    UserFollowMapping.status == RequestStatus.ACCEPTED,
                )
            )
        ).first()

        if not authorized:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="unauthorised"
            )
        
    offset = (page-1)*limit

    followers = session.exec(
        select(User)
        .join(UserFollowMapping, User.id == UserFollowMapping.follower_id)
        .where(
            UserFollowMapping.following_id == user_id,
            UserFollowMapping.status == RequestStatus.ACCEPTED,
        ).offset(offset).limit(limit)
    ).all()
    return followers


@router.get("/{user_id}/following", response_model=list[UserPublic])
def get_following(
    user_id: str,
    user: UserDep,
    session: SessionDep,
    limit:int=Query(10,ge=1,le=100),
    page:int=Query(1,ge=1)
):
    user_to_get = session.get(User, user_id)
    if not user_to_get:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if user_id != str(user.id):
        authorized = session.exec(
            select(UserFollowMapping).where(
                and_(
                    UserFollowMapping.following_id == user_id,
                    UserFollowMapping.follower_id == user.id,
                    UserFollowMapping.status == RequestStatus.ACCEPTED,
                )
            )
        ).first()

        if not authorized:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="unauthorised"
            )
        
    offset = (page-1)*limit

    following = session.exec(
        select(User)
        .join(UserFollowMapping, User.id == UserFollowMapping.following_id)
        .where(
            UserFollowMapping.follower_id == user_id,
            UserFollowMapping.status == RequestStatus.ACCEPTED,
        ).offset(offset).limit(limit)
    ).all()

    return following


@router.delete("/{user_id}/unfollow")
def unfollow_user(user_id: str, user: UserDep, session: SessionDep):
    follow_request = session.get(
        UserFollowMapping, {"follower_id": user.id, "following_id": user_id}
    )
    if not follow_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Follow request not found"
        )
    session.delete(follow_request)
    session.commit()


@router.get("/follow-requests", response_model=list[UserPublic])
def get_follow_requests(user: UserDep, session: SessionDep):
    follow_requests = session.exec(
        select(User)
        .join(UserFollowMapping, UserFollowMapping.follower_id == User.id)
        .where(
            UserFollowMapping.following_id == user.id,
            UserFollowMapping.status == RequestStatus.PENDING,
        )
    ).all()

    return follow_requests


@router.get("/search",response_model=list[UserPublic])
def search_user(
    session: SessionDep,
    search_param : str = Query(None),
    limit: int = Query(10, le=100, ge=1),
    page: int = Query(1, ge=1)
):
    if not search_param: 
        return []
    offset = limit*(page-1)
    query = select(User).where(User.username.startswith(search_param.lower())).offset(offset).limit(limit)
    users = session.exec(query).all()
    return users


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, session: SessionDep):
    if "access_token" not in websocket.headers:
        await websocket.close(code=4001, reason="Missing access_token header")
        return

    access_token = websocket.headers["access_token"].split(" ")[1]

    try:
        payload = verify_token(access_token)
    except Exception as e:
        await websocket.close(code=4002, reason=f"Invalid token: {str(e)}")
        return

    user = session.get(User, payload["sub"])

    await connection_manager.connect(user.id, websocket)

    try:
        while True:
            data = await websocket.receive_json()
            try:
                message_data: SendMessage = SendMessage.model_validate(data)
                new_msg = Chat(
                    sender_id=user.id,
                    receiver_id=message_data.receiver_id,
                    message=message_data.message,
                )
                session.add(new_msg)
                session.commit()
                session.refresh(new_msg)

                await connection_manager.send_message(
                    message_data.receiver_id, new_msg.model_dump_json()
                )
                await connection_manager.send_message(
                    user.id, new_msg.model_dump_json()
                )

            except Exception as e:
                await websocket.send_json({"error": str(e)})
    except Exception as e:
        print(f"connection closed for user {user.id}: {e}")
        await websocket.close(code=1011, reason="Internal server error")
    finally:
        connection_manager.disconnect(user.id)


@router.get("/chat-history/{user_id}", response_model=list[Chat])
def get_chat_history(session: SessionDep, user: UserDep, user_id: str):
    chats = session.exec(
        select(Chat)
        .where(
            or_(
                and_(Chat.sender_id == user_id, Chat.receiver_id == user.id),
                and_(Chat.sender_id == user.id, Chat.receiver_id == user_id),
            )
        )
        .order_by(Chat.created_at)
    ).all()

    return chats
