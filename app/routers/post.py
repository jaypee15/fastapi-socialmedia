from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.schemas import postschemas
from app.models import postmodel, likemodel
from app.database.db import get_db
from app.crud import user_crud

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=list[postschemas.PostOut])
def get_posts(
    db: Session = Depends(get_db),
    current_user=Depends(user_crud.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: str = "",
):
    posts = (
        db.query(postmodel.Post, func.count(likemodel.Like.post_id).label("likes"))
        .join(likemodel.Like, likemodel.Like.post_id == postmodel.Post.id, isouter=True)
        .group_by(postmodel.Post.id)
        .filter(postmodel.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )

    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=postschemas.Post)
def create_post(
    post: postschemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(user_crud.get_current_user),
):
    new_post = postmodel.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=postschemas.PostOut)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(user_crud.get_current_user),
):
    post = (
        db.query(postmodel.Post, func.count(likemodel.Like.post_id).label("likes"))
        .join(likemodel.Like, likemodel.Like.post_id, isouter=True)
        .group_by(postmodel.Post.id)
        .filter(postmodel.Post.id == id)
        .first()
    )

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(user_crud.get_current_user),
):
    post = db.query(postmodel.Post).filter(postmodel.Post.id == id)
    post_query = post.first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exist",
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to perform this action",
        )

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("{/id}", response_model=postschemas.Post)
def update_post(
    id: int,
    updated_post: postschemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(user_crud.get_current_user),
):
    post_query = db.query(postmodel.Post).filter(postmodel.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exist",
        )
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    post_query.update(updated_post.model_dump(), synchronize_session=False)

    db.commit()

    return post_query.first()
