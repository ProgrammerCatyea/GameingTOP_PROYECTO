import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from backend.core.config import settings

DATA_DIR = os.path.join("backend", "data")
os.makedirs(DATA_DIR, exist_ok=True)

DATABASE_URL = settings.DB_URL

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
