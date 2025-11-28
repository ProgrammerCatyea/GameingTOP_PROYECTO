from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from backend.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    nickname = Column(String(50), unique=True, nullable=True, index=True)
    email = Column(String(120), unique=False, nullable=True, index=True)
    pais = Column(String(60), nullable=True)
    edad = Column(Integer, nullable=True)
    nivel_rol = Column(String(60), nullable=True)

    rankings = relationship(
        "Ranking",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    games = relationship(
        "Game",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} nickname={self.nickname!r}>"


