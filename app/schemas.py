from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Esquema de Usuario
class UserBase(BaseModel):
    username: str
    email: str

class LoginRequest(BaseModel):
    email: str
    password: str

class UserCreate(UserBase):
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserResponse(UserBase):
    id: int
    profile_image: Optional[str] = None

    class Config:
        orm_mode = True

# Esquema de Post
class PostBase(BaseModel):
    title: str
    content: str
    media_type: Optional[str] = None
    media_url: Optional[str] = None

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

# Esquema de Like
class LikeBase(BaseModel):
    post_id: int

class LikeResponse(LikeBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True  # ✅ Para compatibilidad con Pydantic v2

# Esquema de Comentario
class CommentBase(BaseModel):
    post_id: int
    text: str

class CommentResponse(CommentBase):
    id: int
    user_id: int
    created_at: str  # ✅ Cambiar de `datetime` a `str`

    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            post_id=obj.post_id,
            text=obj.text,
            user_id=obj.user_id,
            created_at=obj.created_at.isoformat()  # ✅ Convertir `datetime` a `str`
        )

    class Config:
        from_attributes = True  # ✅ Corrección para Pydantic v2