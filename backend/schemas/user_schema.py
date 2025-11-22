from typing import Optional, List
from pydantic import BaseModel
from backend.schemas.ranking_schema import RankingBase
from backend.schemas.game_schema import GameBase

class UserBase(BaseModel):
    id: Optional[int] = None
    nombre: str
    nickname: Optional[str] = None
    pais: Optional[str] = None

    class Config:
        from_attributes = True


class UserDetail(UserBase):
    rankings: List[RankingBase] = []
    games: List[GameBase] = []


class UserCreate(BaseModel):
    nombre: str
    nickname: Optional[str] = None
    pais: Optional[str] = None

    class Config:
        from_attributes = True



class UserUpdate(BaseModel):
    nombre: Optional[str] = None
    nickname: Optional[str] = None
    pais: Optional[str] = None

    class Config:
        from_attributes = True
