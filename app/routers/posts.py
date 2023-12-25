from fastapi import FastAPI, Response, status, HTTPException,Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func

from schemas import postschemas
from models import postmodel
from database.db import get_db
from crud import user_crud

router = APIRouter(
    prefix="posts",
    tags=["Posts"]
)

@router.get("/", response_model=list[postschemas.PostOut])
def get_posts(db: Session=Depends(get_db),
              current_user=Depends(user_crud.get_current_user),
               limit: int=10, skip: int=0, search: str = ""):
    
    posts = db.query(postmodel.Post)