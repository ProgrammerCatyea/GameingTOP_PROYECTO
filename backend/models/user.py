from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from backend.core.database import Base


class Usuario(Base):

    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    nickname = Column(String(50), unique=True, index=True, nullable=True)
    pais = Column(String(50), nullable=True)

    rankings = relationship(
        "Ranking",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )

    juegos = relationship(
        "Juego",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Usuario(nombre='{self.nombre}', nickname='{self.nickname}', pais='{self.pais}')>"
