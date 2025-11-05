from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.core.database import get_db
from backend.models.user import Usuario
from backend.schemas.user_schema import UsuarioBase

router = APIRouter()


@router.get("/", response_model=List[UsuarioBase])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()


@router.get("/{usuario_id}", response_model=UsuarioBase)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario



@router.post("/", response_model=UsuarioBase, status_code=201)
def crear_usuario(payload: UsuarioBase, db: Session = Depends(get_db)):

    if payload.nickname:
        existe = db.query(Usuario).filter(Usuario.nickname == payload.nickname).first()
        if existe:
            raise HTTPException(status_code=400, detail="Ya existe un usuario con ese nickname")

    nuevo = Usuario(
        nombre=payload.nombre,
        nickname=payload.nickname,
        pais=payload.pais
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.delete("/{usuario_id}", status_code=204)
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(usuario)
    db.commit()
    return
