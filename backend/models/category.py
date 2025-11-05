from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from backend.core.database import Base
from backend.models.associations import juego_categoria

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False, unique=True)
    descripcion = Column(String, nullable=True)

    juegos = relationship(
        "Juego",
        secondary=juego_categoria,
        back_populates="categorias",
    )
