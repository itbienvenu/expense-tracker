from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from uuid import uuid4, UUID
from datetime import datetime, UTC

from database.models import User
from database.dbs import get_db
from schemas.UserScheme import UserRegister, UserLogin, UserResponse, UserInfoResponse

from methods.functions import hash_password, verify_password, create_access_token, get_current_user
from methods.password import is_strong_password, password_strength_meter

router = APIRouter(prefix="/auth", tags=["Authentication"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Register endpoint

@router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    # Check if email exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    is_strong, errors = is_strong_password(user.password)
    if not is_strong:
        # Return error as a normal 200 response with error details
        return {
            "detail": password_strength_meter(user.password)[1]
        }
    new_user = User(
        id=uuid4(),
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
        created_at = datetime.now(UTC)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"detail":"User created well"}


# Login Endpoint

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.hashed_password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # generate JWT token
    token_data = {"sub": str(db_user.id)} 
    token = create_access_token(token_data)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserInfoResponse)
async def get_me(current_user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Get current user information from JWT token
    """
    try:
        user_uuid = UUID(current_user_id)
        user = db.query(User).filter(User.id == user_uuid).first()
        return {
            "id": user.id,
            "username": user.username,
            "email":user.email,
            "created_at":user.created_at
        }
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID format"
        )    