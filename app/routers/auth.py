from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schemas import tokenschemas
from app.models import usermodel
from app.database.db import get_db
from app.utils import utils
from app.crud import user_crud

router = APIRouter(tags=["Authentication"])


@router.post("login", response_model=tokenschemas.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = (
        db.query(usermodel.User)
        .filter(usermodel.User.email == user_credentials.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials"
        )
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, details="Invalid credentials"
        )

    access_token = user_crud.create_access_token(data={"user_id": user.id})

    return {"acces_token": access_token, "token_type": "bearer"}
