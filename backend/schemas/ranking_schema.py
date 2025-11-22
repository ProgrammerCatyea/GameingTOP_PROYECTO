from typing import Optional, List
from pydantic import BaseModel
from backend.schemas.game_schema import GameBase


class RankingBase(BaseModel):
    id: Optional[int] = None
    nombre: str
    descripcion: Optional[str] = None
    tipo: Optional[str] = "global"   
    user_id: Optional[int] = None    

    class Config:
        from_attributes = True



class RankingDetail(RankingBase):
    games: List[GameBase] = []     



class RankingCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    tipo: Optional[str] = "global"
    user_id: Optional[int] = None

    class Config:
        from_attributes = True


class RankingUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    tipo: Optional[str] = None
    user_id: Optional[int] = None

    class Config:
        from_attributes = True
