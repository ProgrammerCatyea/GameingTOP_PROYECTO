from typing import Optional, List
from pydantic import BaseModel


class UserBase(BaseModel):
    id: Optional[int] = None
    nombre: str
    nickname: Optional[str] = None
    pais: Optional[str] = None

    class Config:
        from_attributes = True


class UserDetail(UserBase):
    rankings: Optional[List[str]] = None
    juegos: Optional[List[str]] = None
