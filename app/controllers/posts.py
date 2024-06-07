from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import HTTPException, Depends
from datetime import datetime, timedelta

from db import schemas

from db import models

from utils import cache_response, get_cached_response


def create_post(db: Session, post: schemas.PostCreate, user_id: int):
    db_post = models.Post(**post.dict(), owner_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_posts(db: Session, user_id: int):
    posts = get_cached_response("posts")
    if not posts:
        posts = db.query(models.Post).filter(models.Post.owner_id == user_id).all()
        cache_response("posts", posts)

    return posts


def delete_post(db: Session, post_id: int, user_id: int):
    post = (
        db.query(models.Post)
        .filter(models.Post.id == post_id, models.Post.owner_id == user_id)
        .first()
    )
    if post:
        db.delete(post)
        db.commit()
        return post
    else:
        return None
