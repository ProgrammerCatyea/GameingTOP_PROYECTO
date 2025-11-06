from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.core.dependencies import get_database
from backend.models.user import Usuario
from backend.schemas.user_schema import UsuarioBase

router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"]
)

@router.get("/", response_model=List[UsuarioBase])
def listar_usuarios(db: Session = Depends(get_database)):
    usuarios = db.query(Usuario).all()
    return usuarios

@router.get("/{usuario_id}", response_model=UsuarioBase)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_database)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return usuario


@router.post("/", response_model=UsuarioBase, status_code=status.HTTP_201_CREATED)
def crear_usuario(payload: UsuarioBase, db: Session = Depends(get_database)):
    if payload.nickname:
        existe = db.query(Usuario).filter(Usuario.nickname == payload.nickname).first()
        if existe:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un usuario con ese nickname"
            )

    nuevo = Usuario(
        nombre=payload.nombre,
        nickname=payload.nickname,
        pais=payload.pais
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_database)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    db.delete(usuario)
    db.commit()
    return None
