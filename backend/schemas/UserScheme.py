from pydantic import BaseModel, EmailStr, constr, validator
from uuid import UUID
from typing import Optional
from methods.password import is_strong_password, password_strength_meter
from datetime import datetime


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    hashed_password: str

class UserResponse(BaseModel):
    message: str

    class Config:
        orm_mode = True
class UserInfoResponse(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True        