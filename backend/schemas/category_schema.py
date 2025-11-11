from typing import Optional, List
from pydantic import BaseModel

class CategoryBase(BaseModel):
    id: Optional[int] = None
    nombre: str
    descripcion: Optional[str] = None

    class Config:
        from_attributes = True

class CategoryDetail(CategoryBase):
    juegos: Optional[List[str]] = None
