from sqlalchemy import Table, Column, Integer, ForeignKey
from backend.core.database import Base

game_category = Table(
    "juego_categoria",
    Base.metadata,
    Column("juego_id", Integer, ForeignKey("juegos.id"), primary_key=True),
    Column("categoria_id", Integer, ForeignKey("categorias.id"), primary_key=True)
)
ranking_game = Table(
    "ranking_juego",
    Base.metadata,
    Column("ranking_id", Integer, ForeignKey("rankings.id"), primary_key=True),
    Column("juego_id", Integer, ForeignKey("juegos.id"), primary_key=True),
    Column("posicion", Integer, nullable=True),
    Column("score", Integer, nullable=True)
)
