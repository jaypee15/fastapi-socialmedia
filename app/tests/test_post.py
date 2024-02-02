import json
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database.db import get_db, Base


# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False},  poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def overide_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = overide_get_db

client = TestClient(app)

def get_test_token(client: TestClient, email: str, password: str):
    login_data = {
        "username": email,
        "password": password,
    }

    response = client.post("/token", data=login_data)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_post():


    user_data = {
        "email": "test@example.com",
        "password": "testpassword",
    }
    client.post("/users/", json=user_data)

    # Authenticate the user
    auth_headers = get_test_token(client, email=user_data["email"], password=user_data["password"])


    post_data = {
        "title": "Test Post",
        "content": "This is a test post.",
    }
    response = client.post(
        "/posts/",
        json=post_data, headers=auth_headers
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Test Post"


# def test_get_posts():
#     response = client.get("/posts/")
#     assert response.status_code == 200
#     assert len(response.json()) > 0


# def test_get_post():
#     response = client.get("/posts/1")
#     assert response.status_code == 200
#     assert "title" in response.json()

# def test_update_post():
#     post_data = {
#         "title": "Updated Post",
#         "content": "This is an updated post.",
#     }
#     response = client.put(
#         "/posts/1",
#         json=post_data
#     )
#     assert response.status_code == 200
#     assert response.json()["title"] == "Updated Post"

# def test_delete_post():
#     response = client.delete("/posts/1")
#     assert response.status_code == 204
    

