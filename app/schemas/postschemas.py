from pydantic import BaseModel
from datetime import datetime

from app.schemas.userschemas import UserOutSchema


class PostBase(BaseModel):
    title: str
    content: str
    published: bool


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOutSchema

    class Config:
        from_attributes = True


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True
