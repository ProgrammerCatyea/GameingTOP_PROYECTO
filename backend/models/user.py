from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from backend.core.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    nickname = Column(String, unique=True, index=True, nullable=True)
    pais = Column(String, nullable=True)

    rankings = relationship("Ranking", back_populates="usuario", cascade="all, delete-orphan")
