from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from auth import hash_password, verify_password, create_access_token
import crud, schemas
from database import SessionLocal
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from models import User
from auth import get_current_user
from typing import List


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_exists = db.query(User).filter(User.username == user.username).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="Username already exists")
    user.password = hash_password(user.password)
    return crud.create_user(db, user)

@router.post("/login", response_model=schemas.Token)
def login(user_login: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, user_login.username)
    if not user or not verify_password(user_login.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=30))
    return {"access_token": token, "token_type": "bearer"}


@router.get("/", response_model=List[schemas.UserOut])
def get_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.get_users(db)

@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

