from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.core.dependencies import get_database
from backend.models.user import User
from backend.schemas.user_schema import (
    UserCreate,
    UserUpdate,
    UserDetail,
)

router = APIRouter(
    prefix="",
    tags=["Usuarios"]
)


@router.get("/", response_model=List[UserDetail])
def list_users(db: Session = Depends(get_database)):
    """
    Listar todos los usuarios.
    """
    users = db.query(User).all()
    return users


@router.get("/{usuario_id}", response_model=UserDetail)
def get_user(usuario_id: int, db: Session = Depends(get_database)):
    user = db.query(User).filter(User.id == usuario_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.post("/", response_model=UserDetail, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_database)):
    
    if payload.nickname:
        existing = (
            db.query(User)
            .filter(User.nickname == payload.nickname)
            .first()
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this nickname already exists"
            )

    new_user = User(
        nombre=payload.nombre,
        nickname=payload.nickname,
        email=payload.email,
        pais=payload.pais,
        edad=payload.edad,
        nivel_rol=payload.nivel_rol,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.put("/{usuario_id}", response_model=UserDetail)
def update_user(
    usuario_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_database),
):

    user = db.query(User).filter(User.id == usuario_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if payload.nickname:
        existing = (
            db.query(User)
            .filter(User.nickname == payload.nickname, User.id != usuario_id)
            .first()
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this nickname already exists"
            )

    for field, value in payload.dict(exclude_unset=True).items():
        if hasattr(user, field):
            setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(usuario_id: int, db: Session = Depends(get_database)):
    """
    Eliminar un usuario por ID.
    """
    user = db.query(User).filter(User.id == usuario_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    db.delete(user)
    db.commit()
    return None
