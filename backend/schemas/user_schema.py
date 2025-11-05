from typing import Optional, List
from pydantic import BaseModel

class UsuarioBase(BaseModel):
    id: Optional[int] = None
    nombre: str
    nickname: Optional[str] = None
    pais: Optional[str] = None

    class Config:
        from_attributes = True
