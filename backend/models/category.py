from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from backend.core.database import Base
from backend.models.associations import game_category


class Category(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(String(255), nullable=True)

    games = relationship(
        "Game",
        secondary=game_category,
        back_populates="categories",
        lazy="joined"  
    )

    def __repr__(self):
        return f"<Category(nombre='{self.nombre}', descripcion='{self.descripcion}')>"
