from typing import Optional
from pydantic import BaseModel

class CategoriaBase(BaseModel):
    id: Optional[int] = None
    nombre: str
    descripcion: Optional[str] = None

    class Config:
        from_attributes = True
