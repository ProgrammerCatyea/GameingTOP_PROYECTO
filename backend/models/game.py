from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.core.database import Base
from backend.models.associations import juego_categoria, ranking_juego


class Juego(Base):
  
    __tablename__ = "juegos"

    id = Column(Integer, primary_key=True, index=True)
    appid = Column(Integer, index=True, nullable=True)   
    nombre = Column(String(150), nullable=False, index=True)
    plataforma = Column(String(100), nullable=True)
    desarrollador = Column(String(150), nullable=True)
    genero_principal = Column(String(100), nullable=True)


    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    usuario = relationship("Usuario", back_populates="juegos")

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


    def __repr__(self):
        return f"<Juego(nombre='{self.nombre}', plataforma='{self.plataforma}', genero='{self.genero_principal}')>"

