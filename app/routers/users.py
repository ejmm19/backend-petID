from fastapi import APIRouter, Depends, HTTPException  # ✅ Agregar APIRouter aquí
from fastapi.security import OAuth2PasswordRequestForm  # ✅ Agregar esta línea
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
from app.auth import authenticate_user, create_access_token
from app.auth import authenticate_user, create_access_token, get_current_user  # ✅ Asegurar esta importación



router = APIRouter(prefix="/users", tags=["Users"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Verificar si el usuario ya existe
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/login", response_model=schemas.Token)
def login(request: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, request.email, request.password)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(hours=1))
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserResponse)
def read_users_me(current_user: schemas.UserResponse = Depends(get_current_user)):  # ✅ Se usará get_current_user correctamente
    return current_user