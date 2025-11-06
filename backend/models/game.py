from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.core.database import Base
from backend.models.associations import game_category, ranking_game


class Game(Base):
    __tablename__ = "juegos"
    id = Column(Integer, primary_key=True, index=True)
    appid = Column(Integer, index=True, nullable=True)
    nombre = Column(String(150), nullable=False, index=True)
    plataforma = Column(String(100), nullable=True)
    desarrollador = Column(String(150), nullable=True)
    genero_principal = Column(String(100), nullable=True)

    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    user = relationship("User", back_populates="games")

    categories = relationship(
        "Category",
        secondary=game_category,
        back_populates="games",
    )

    rankings = relationship(
        "Ranking",
        secondary=ranking_game,
        back_populates="games",
        viewonly=False,
    )

    def __repr__(self):
        return (
            f"<Game(nombre='{self.nombre}', plataforma='{self.plataforma}', "
            f"desarrollador='{self.desarrollador}', genero_principal='{self.genero_principal}')>"
        )

