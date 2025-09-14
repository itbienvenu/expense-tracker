from pydantic import BaseModel, EmailStr, constr
from uuid import UUID
from typing import Optional


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    is_active: bool

    class Config:
        orm_mode = True
