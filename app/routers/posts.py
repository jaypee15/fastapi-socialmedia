from fastapi import FastAPI, Response, status, HTTPException,Depends, APIRouter

router = APIRouter(
    prefix="posts",
    tags=["Posts"]
)

@router.get("/", response_model=)