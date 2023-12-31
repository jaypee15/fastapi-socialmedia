from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import post, user, like
from app.database.db import init_db



app = FastAPI()

origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

init_db()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(like.router)