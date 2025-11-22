from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.core.dependencies import get_database
from backend.models.category import Category
from backend.schemas.category_schema import (
    CategoryBase,
    CategoryDetail,
    CategoryCreate,
    CategoryUpdate
)

router = APIRouter()


@router.get("/", response_model=List[CategoryDetail])
def list_categories(db: Session = Depends(get_database)):
    categorias = db.query(Category).all()
    return categorias


@router.get("/{categoria_id}", response_model=CategoryDetail)
def get_category(categoria_id: int, db: Session = Depends(get_database)):
    categoria = db.query(Category).filter(Category.id == categoria_id).first()
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La categoría no existe."
        )
    return categoria


@router.post("/", response_model=CategoryDetail, status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreate, db: Session = Depends(get_database)):
    existe = db.query(Category).filter(Category.nombre == payload.nombre).first()
    if existe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una categoría con ese nombre."
        )

    nueva = Category(nombre=payload.nombre, descripcion=payload.descripcion)
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


@router.put("/{categoria_id}", response_model=CategoryDetail)
def update_category(categoria_id: int, payload: CategoryUpdate, db: Session = Depends(get_database)):
    categoria = db.query(Category).filter(Category.id == categoria_id).first()

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La categoría no existe."
        )

    if payload.nombre is not None:
        categoria.nombre = payload.nombre
    if payload.descripcion is not None:
        categoria.descripcion = payload.descripcion

    db.commit()
    db.refresh(categoria)
    return categoria


@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(categoria_id: int, db: Session = Depends(get_database)):
    categoria = db.query(Category).filter(Category.id == categoria_id).first()

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La categoría no existe."
        )

    db.delete(categoria)
    db.commit()
    return None
