from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.core.dependencies import get_database
from backend.models.user import User
from backend.schemas.user_schema import UserBase

router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"]
)


@router.get("/", response_model=List[UserBase])
def list_users(db: Session = Depends(get_database)):
    users = db.query(User).all()
    return users


@router.get("/{usuario_id}", response_model=UserBase)
def get_user(usuario_id: int, db: Session = Depends(get_database)):
    user = db.query(User).filter(User.id == usuario_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.post("/", response_model=UserBase, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserBase, db: Session = Depends(get_database)):
    if payload.nickname:
        existing = db.query(User).filter(User.nickname == payload.nickname).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this nickname already exists"
            )

    new_user = User(
        nombre=payload.nombre,
        nickname=payload.nickname,
        pais=payload.pais
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(usuario_id: int, db: Session = Depends(get_database)):
    user = db.query(User).filter(User.id == usuario_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    db.delete(user)
    db.commit()
    return None
