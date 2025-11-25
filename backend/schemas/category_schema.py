from typing import Optional
from pydantic import BaseModel


class CategoryBase(BaseModel):
    id: Optional[int] = None
    nombre: str
    descripcion: Optional[str] = None

    class Config:
        from_attributes = True



class CategoryDetail(CategoryBase):
    pass



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

