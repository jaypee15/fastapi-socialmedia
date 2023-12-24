from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
class UserOut(UserBase):
    id: str
    created_at: datetime

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str


class UserLogin(UserBase):
    password: str