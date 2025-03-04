from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.auth import get_current_user

router = APIRouter(prefix="/comments", tags=["Comments"])

@router.post("/", response_model=schemas.CommentResponse)
def add_comment(comment: schemas.CommentBase, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_comment = models.Comment(user_id=current_user.id, post_id=comment.post_id, text=comment.text)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


@router.get("/{post_id}", response_model=list[schemas.CommentResponse])
def get_comments(post_id: int, db: Session = Depends(get_db)):
    comments = db.query(models.Comment).filter(models.Comment.post_id == post_id).all()

    # ✅ Convertir `created_at` a string antes de devolverlo
    return [schemas.CommentResponse.from_orm(comment) for comment in comments]
