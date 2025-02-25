from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.auth_schema import RegisterRequest, LoginRequest, TokenResponse
from schemas.user_schema import UserResponse
from models.user_model import User
from database.database import get_db
from utils.security import hash_password, verify_password, create_access_token

router = APIRouter()

@router.post("/auth/register", response_model=UserResponse)
def register_user(user: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed_pwd = hash_password(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_pwd)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    print(db_user)
    return db_user

@router.post("/auth/login", response_model=TokenResponse)
def login_user(credentials: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == credentials.username).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
