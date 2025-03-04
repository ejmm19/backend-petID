from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.auth import get_current_user

router = APIRouter(prefix="/likes", tags=["Likes"])


@router.post("/", response_model=schemas.LikeResponse)
def like_post(like: schemas.LikeBase, db: Session = Depends(get_db),
              current_user: models.User = Depends(get_current_user)):
    existing_like = db.query(models.Like).filter(
        models.Like.user_id == current_user.id, models.Like.post_id == like.post_id
    ).first()

    if existing_like:
        raise HTTPException(status_code=400, detail="You already liked this post")

    db_like = models.Like(user_id=current_user.id, post_id=like.post_id)
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like


@router.delete("/{post_id}")
def unlike_post(post_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    like = db.query(models.Like).filter(models.Like.user_id == current_user.id, models.Like.post_id == post_id).first()

    if not like:
        raise HTTPException(status_code=404, detail="Like not found")

    db.delete(like)
    db.commit()
    return {"message": "Like removed"}
