from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.core.database import Base
from backend.models.associations import ranking_juego

class Ranking(Base):
    __tablename__ = "rankings"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False, index=True)
    descripcion = Column(String, nullable=True)
    tipo = Column(String, nullable=True) 
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    usuario = relationship("Usuario", back_populates="rankings")

    juegos = relationship(
        "Juego",
        secondary=ranking_juego,
        back_populates="rankings",
        viewonly=False,
    )
