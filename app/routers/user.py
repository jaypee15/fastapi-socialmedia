from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app.schemas import userschemas
from app.models import usermodel
from app.database.db import get_db
from app.utils import utils


router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=userschemas.UserOut
)
def create_user(user: userschemas.UserCreate, db: Session = Depends(get_db)):
    # Hash the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = usermodel.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=userschemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(usermodel.User).filter(usermodel.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id {id} does not exist",
        )

    return user
