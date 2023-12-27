from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from app.models.postmodel import Post
from app.models.usermodel import User   # Import the Post model from your models module
from app.database.db import engine  # Import the database engine
import json

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_post(db, post_data):
    try:
        post = Post(**post_data)
        db.add(post)
        db.commit()
        db.refresh(post)
        print(f"Added post with ID: {post.id}")
    except IntegrityError:
        print(f"Post already exists in the database with title: {post_data['title']}")

def load_posts():
    with open("posts_data.json", "r") as file:
        posts_data = json.load(file)

    db = SessionLocal()

    try:
        for post_data in posts_data:
            create_post(db, post_data)
    finally:
        db.close()

if __name__ == "__main__":
    load_posts()
