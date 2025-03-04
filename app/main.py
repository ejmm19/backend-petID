from fastapi import FastAPI
from app.routers import users, posts, likes, comments  # ✅ Asegurar esta importación
from app.database import engine
from app.models import Base

# Crear la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Agregar routers
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(likes.router)
app.include_router(comments.router)

@app.get("/")
def read_root():
    return {"message": "FastAPI App with JWT and MySQL"}
