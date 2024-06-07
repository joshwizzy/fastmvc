from datetime import timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from controllers import users
from db import schemas

from db.database import get_db

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/signup", response_model=schemas.UserOut)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = users.get_user(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return users.create_user(db=db, user=user)


@router.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = users.authenticate_user(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=users.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = users.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/posts", response_model=schemas.PostOut)
def add_post(
    post: schemas.PostCreate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    current_user = users.get_current_user(db, token)
    return users.create_post(db=db, post=post, user_id=current_user.id)


@router.get("/posts", response_model=List[schemas.PostOut])
def get_posts(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    current_user = users.get_current_user(db, token)
    return users.get_posts(db=db, user_id=current_user.id)


@router.delete("/posts/{post_id}", response_model=schemas.PostOut)
def delete_post(
    post_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    current_user = users.get_current_user(db, token)
    post = users.delete_post(db=db, post_id=post_id, user_id=current_user.id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post
