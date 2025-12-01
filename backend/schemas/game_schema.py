from typing import List, Optional
from pydantic import BaseModel
from backend.schemas.category_schema import CategoryBase


class GameBase(BaseModel):
    id: Optional[int] = None
    appid: Optional[int] = None
    nombre: str
    plataforma: Optional[str] = "Steam/PC"
    desarrollador: Optional[str] = None
    genero_principal: Optional[str] = None

    class Config:
        from_attributes = True


class GameDetail(GameBase):
    categorias: List[CategoryBase] = []



class GameCreate(BaseModel):
    nombre: str
    plataforma: Optional[str] = "Steam/PC"
    desarrollador: Optional[str] = None
    genero_principal: Optional[str] = None

    categorias_ids: List[int] = []      
    user_id: Optional[int] = None       

    class Config:
        from_attributes = True



class GameUpdate(BaseModel):
    nombre: Optional[str] = None
    plataforma: Optional[str] = None
    desarrollador: Optional[str] = None
    genero_principal: Optional[str] = None
    categorias_ids: Optional[List[int]] = None
    user_id: Optional[int] = None

    class Config:
        from_attributes = True



class GameUpdate(BaseModel):
    nombre: Optional[str] = None
    plataforma: Optional[str] = None
    desarrollador: Optional[str] = None
    genero_principal: Optional[str] = None
    categorias_ids: Optional[List[int]] = None
    user_id: Optional[int] = None

    class Config:
        from_attributes = True
