from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.core.dependencies import get_database
from backend.models.user import User
from backend.schemas.user_schema import (
    UserBase,
    UserDetail,
    UserCreate,
    UserUpdate,
)

router = APIRouter()



@router.get("/", response_model=List[UserDetail])
def list_users(db: Session = Depends(get_database)):
    usuarios = db.query(User).all()
    return usuarios



@router.get("/{usuario_id}", response_model=UserDetail)
def get_user(usuario_id: int, db: Session = Depends(get_database)):
    usuario = db.query(User).filter(User.id == usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario no existe.",
        )
    return usuario



@router.post("/", response_model=UserDetail, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_database)):
    if payload.nickname:
        existente = (
            db.query(User)
            .filter(User.nickname == payload.nickname)
            .first()
        )
        if existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un usuario con ese nickname.",
            )

    nuevo = User(
        nombre=payload.nombre,
        nickname=payload.nickname,
        pais=payload.pais,
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo



@router.put("/{usuario_id}", response_model=UserDetail)
def update_user(
    usuario_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_database),
):
    usuario = db.query(User).filter(User.id == usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario no existe.",
        )

    if payload.nombre is not None:
        usuario.nombre = payload.nombre
    if payload.nickname is not None:
    
        existente = (
            db.query(User)
            .filter(User.nickname == payload.nickname, User.id != usuario_id)
            .first()
        )
        if existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe otro usuario con ese nickname.",
            )
        usuario.nickname = payload.nickname
    if payload.pais is not None:
        usuario.pais = payload.pais

    db.commit()
    db.refresh(usuario)
    return usuario



@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(usuario_id: int, db: Session = Depends(get_database)):
    usuario = db.query(User).filter(User.id == usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario no existe.",
        )

    db.delete(usuario)
    db.commit()
    return None
