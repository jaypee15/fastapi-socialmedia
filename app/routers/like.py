from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schemas import likeschemas
from app.models import postmodel, likemodel
from app.database.db import get_db
from app.utils import utils
from app.crud import user_crud

router = APIRouter(prefix="/like", tags=["Like"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def like(
    like: likeschemas.Like,
    db: Session = Depends(get_db),
    current_user: int = Depends(user_crud.get_current_user),
):
    post = db.query(postmodel.Post).filter(postmodel.Post.id == like.post_id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {like.post_id} does not exist",
        )

    like_query = db.query(likemodel.Like).filter(
        likemodel.Like.post_id == like.post_id,
        likemodel.Like.user_id == current_user.id,
    )

    found_like = like_query.first()
    if like.dir == 1:
        if found_like:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                details="user {current_user.id} already liked post {like.post_id}",
            )
        new_like = likemodel.Like(post_id=like.post_id, user_id=current_user.id)
        db.add(new_like)
        db.commit()

        return {"message": "successfully liked post"}
    else:
        if not found_like:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="like does not exist"
            )
        like_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfuly unliked post"}
