from pydantic import BaseModel, EmailStr, constr, validator
from uuid import UUID
from typing import Optional
from methods.password import is_strong_password, password_strength_meter

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