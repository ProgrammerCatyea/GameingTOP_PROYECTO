from typing import List, Optional
from pydantic import BaseModel
from backend.schemas.category_schema import CategoriaBase


class JuegoBase(BaseModel):
    id: Optional[int] = None
    appid: Optional[int] = None          
    plataforma: Optional[str] = "Steam/PC"
    desarrollador: Optional[str] = None
    genero_principal: Optional[str] = None

    class Config:
        from_attributes = True

class JuegoDetail(JuegoBase):
    categorias: List[CategoriaBase] = []

class JuegoCreate(BaseModel):
    nombre: str
    plataforma: Optional[str] = "Steam/PC"
    desarrollador: Optional[str] = None
    genero_principal: Optional[str] = None
    categorias_ids: List[int] = []  

    class Config:
        from_attributes = True

class JuegoUpdate(BaseModel):
    nombre: Optional[str] = None
    plataforma: Optional[str] = None
    desarrollador: Optional[str] = None
    genero_principal: Optional[str] = None
    categorias_ids: Optional[List[int]] = None 

    class Config:
        from_attributes = True
