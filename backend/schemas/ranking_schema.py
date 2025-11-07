from typing import Optional, List
from pydantic import BaseModel
from backend.schemas.game_schema import GameBase

class RankingBase(BaseModel):
    id: Optional[int] = None
    nombre: str
    descripcion: Optional[str] = None
    tipo: Optional[str] = "global"
    usuario_id: Optional[int] = None

    class Config:
        from_attributes = True


class RankingDetail(RankingBase):
    juegos: List[GameBase] = []
