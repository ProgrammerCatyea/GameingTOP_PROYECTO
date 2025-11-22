from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from backend.core.database import Base


class User(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    nickname = Column(String(50), unique=True, index=True, nullable=True)
    pais = Column(String(50), nullable=True)

    rankings = relationship(
        "Ranking",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="joined"
    )

    games = relationship(
        "Game",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="joined"
    )

    def __repr__(self):
        return f"<User(nombre='{self.nombre}', nickname='{self.nickname}', pais='{self.pais}')>"


