import cloudinary.uploader
from fastapi import APIRouter, Form, HTTPException, UploadFile, status
from database import SessionDep
from models import Post, PostImageMapping, Comment
from schema import PostCreate, CommentWithUser
from security import UserDep

router = APIRouter(
    prefix="/post",
    tags=["post"],
)


@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
def create_post(
    session: SessionDep,
    user: UserDep,
    text: str = Form(),
    image: UploadFile | None = None,
):
    # Validate the image file
    if image and image.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image format. Only JPEG and PNG are allowed.",
        )
    image_url = None
    if image:
        try:
            upload_result = cloudinary.uploader.upload(image.file, folder="posts")
            image_url = upload_result.get("secure_url")
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Image upload failed: {str(e)}"
            )

    new_post = Post(
        text=text,
        user_id=user.id,
    )
    session.add(new_post)
    session.commit()
    if image_url:
        session.add(PostImageMapping(post_id=new_post.id, image_url=image_url))
        session.commit()
    return new_post


@router.delete("/{post_id}/delete")
def delete_post(post_id: str, session: SessionDep, user: UserDep):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    if post.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="unauthorised"
        )

    session.delete(post)
    session.commit()


@router.post("/{post_id}/like")
def like_post(post_id: str, session: SessionDep, _: UserDep):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    
    
@router.post("/{post_id}/comment",status_code=status.HTTP_201_CREATED,response_model=Comment)
def add_comment_to_post(post_data:PostCreate, post_id: str, session: SessionDep, user: UserDep):

    post = session.get(Post,post_id)
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="post not found")
    
    comment = Comment(text=post_data.text, user_id=user.id, post_id=post_id)
    session.add(comment)
    session.commit()
    session.refresh(comment)
    return comment


@router.get("/{post_id}/comments",response_model=list[CommentWithUser])
def get_post_comments(post_id: str, session: SessionDep):
    post = session.get(Post,post_id)
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="post not found")
    
    return post.comments