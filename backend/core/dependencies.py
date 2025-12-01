from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.core.config import settings

def get_database() -> Session:
    yield from get_db()

def get_settings():
    return settings
