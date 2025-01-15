from fastapi import APIRouter,HTTPException,status,Query,WebSocket
from models.user import *
from database import SessionDep
from security import create_token,Token,hash_password,verify_password,UserDep
from sqlmodel import select
from sqlalchemy import exc

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

@router.post(
    "/register",
    response_model=Token,
    status_code=status.HTTP_201_CREATED
)
def register_user(userCreate: UserCreate,session: SessionDep):
    try:
        new_user = User(
            first_name = userCreate.first_name,
            last_name = userCreate.last_name,
            email = userCreate.email,
            username = userCreate.username,
            password = hash_password(userCreate.password),
            bio = userCreate.bio,
            profile_image = userCreate.profile_image
        )
        session.add(new_user)
        session.commit()
    except exc.IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400,detail="User already exists")
    except Exception as e:
        session.rollback()
        raise e
    return Token(access_token=create_token(str(new_user.id)))


@router.post(
    "/login",
    response_model=Token
)
def login_user(userLogin: UserLogin,session: SessionDep):
    user = session.exec(select(User).where(User.username == userLogin.username)).first()
    if not user or not verify_password(userLogin.password,user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User does not exist")
    return Token(access_token=create_token(str(user.id)))
    

@router.get(
    "/profile/me",
    response_model=UserWithPosts
)
def get_profile(user: UserDep):
    return user

# @router.get("/feed")
# def get_feed(
#     user: UserDep,
#     session: SessionDep,
#     limit: int = Query(10), 
#     offset: int = Query(0)
# ):
#     query = select(Post).join(
#         UserFollowMapping,User.id == UserFollowMapping.following_id
#     ).where(
#         UserFollowMapping.follower_id == user.id,
#         UserFollowMapping.status == RequestStatus.ACCEPTED
#     ).order_by(Post.)
    

@router.post("/{user_id}/follow",status_code=status.HTTP_201_CREATED)
def follow_user(user_id: str,user: UserDep,session: SessionDep): 
    user_to_follow = session.get(User,user_id)
    if not user_to_follow:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    follow_request = UserFollowMapping(follower_id=user.id,following_id=user_id)
    session.add(follow_request)
    session.commit()


@router.post("/{user_id}/accept")
def accept_follow_request(user_id: str,user: UserDep,session: SessionDep):
    follow_request = session.get(UserFollowMapping,{"follower_id":user_id,"following_id":user.id})
    if not follow_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Follow request not found")
    follow_request.status = RequestStatus.ACCEPTED
    session.commit()


@router.post("/{user_id}/reject")
def reject_follow_request(user_id: str,user: UserDep,session: SessionDep):
    follow_request = session.get(UserFollowMapping,{"follower_id":user_id,"following_id":user.id})
    if not follow_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Follow request not found")
    follow_request.status = RequestStatus.REJECTED
    session.commit()


@router.get("/{user_id}/followers",response_model=list[UserPublic])
def get_followers(user_id: str,user: UserDep,session: SessionDep):

    user_to_get = session.get(User,user_id)
    if not user_to_get:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")

    if user_id != str(user.id):
        authorized = session.exec(
            select(UserFollowMapping).where(
                and_(
                    UserFollowMapping.following_id == user_id,
                    UserFollowMapping.follower_id == user.id,
                    UserFollowMapping.status == RequestStatus.ACCEPTED
                )
            )
        ).first()

        if not authorized:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="unauthorised")

    followers = session.exec(
        select(User).join(UserFollowMapping,User.id == UserFollowMapping.follower_id).where(
            UserFollowMapping.following_id == user_id,
            UserFollowMapping.status == RequestStatus.ACCEPTED
        )
    ).all()
    return followers


@router.get("/{user_id}/following",response_model=list[UserPublic])
def get_following(user_id:str,user:UserDep,session:SessionDep):

    user_to_get = session.get(User,user_id)
    if not user_to_get:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")

    if user_id != str(user.id):
        authorized = session.exec(
            select(UserFollowMapping).where(
                and_(
                    UserFollowMapping.following_id == user_id,
                    UserFollowMapping.follower_id == user.id,
                    UserFollowMapping.status == RequestStatus.ACCEPTED
                )
            )
        ).first()

        if not authorized:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="unauthorised")

    following = session.exec(
        select(User).join(UserFollowMapping,User.id == UserFollowMapping.following_id).where(
            UserFollowMapping.follower_id == user_id,
            UserFollowMapping.status == RequestStatus.ACCEPTED
        )
    ).all()

    return following


@router.delete("/{user_id}/unfollow")
def unfollow_user(user_id: str,user: UserDep,session: SessionDep):
    follow_request = session.get(UserFollowMapping,{"follower_id":user.id,"following_id":user_id})
    if not follow_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Follow request not found")
    session.delete(follow_request)
    session.commit()


@router.get("/follow-requests",response_model=list[UserPublic])
def get_follow_requests(user: UserDep,session: SessionDep):
    follow_requests = session.exec(
        select(User).join(UserFollowMapping,UserFollowMapping.follower_id == User.id).where(
            UserFollowMapping.following_id == user.id,
            UserFollowMapping.status == RequestStatus.PENDING   
        )
    ).all()

    return follow_requests

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")

