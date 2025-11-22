from typing import Optional, List
from pydantic import BaseModel
from backend.schemas.game_schema import GameBase


class CategoryBase(BaseModel):
    id: Optional[int] = None
    nombre: str
    descripcion: Optional[str] = None

    class Config:
        from_attributes = True


class CategoryDetail(CategoryBase):
    juegos: List[GameBase] = []


class CategoryCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

    class Config:
        from_attributes = True


class CategoryUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None

    class Config:
        from_attributes = True
