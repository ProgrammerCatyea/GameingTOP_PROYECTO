from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from backend.core.database import Base
from backend.models.associations import juego_categoria, ranking_juego

class Juego(Base):
    __tablename__ = "juegos"

    id = Column(Integer, primary_key=True, index=True)

    appid = Column(Integer, index=True, nullable=True)  
    nombre = Column(String, nullable=False, index=True)
    plataforma = Column(String, nullable=True)          
    desarrollador = Column(String, nullable=True)
    genero_principal = Column(String, nullable=True)

    categorias = relationship(
        "Categoria",
        secondary=juego_categoria,
        back_populates="juegos",
    )

    rankings = relationship(
        "Ranking",
        secondary=ranking_juego,
        back_populates="juegos",
        viewonly=False,
    )
