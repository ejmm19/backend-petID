from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import time

# Configuración de la base de datos
DB_USER = os.getenv("MYSQL_USER", "root")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD", "root")
DB_HOST = os.getenv("MYSQL_HOST", "db")  # Nombre del servicio en docker-compose
DB_PORT = os.getenv("MYSQL_PORT", "3306")
DB_NAME = os.getenv("MYSQL_DATABASE", "fastapi_db")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Función para obtener la sesión de la BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Esperar hasta que la base de datos esté disponible
def wait_for_db():
    retries = 10
    while retries > 0:
        try:
            with engine.connect() as connection:
                print("✅ Conexión a MySQL exitosa!")
                return
        except Exception as e:
            print(f"❌ Error de conexión a MySQL: {e}")
            retries -= 1
            time.sleep(5)
    print("🚨 No se pudo conectar a MySQL después de varios intentos.")

wait_for_db()
