from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.core.dependencies import get_database
from backend.models.category import Category
from backend.schemas.category_schema import CategoryBase

router = APIRouter(
    prefix="",
    tags=["Categorías"]
)


@router.get("/", response_model=List[CategoryBase])
def list_categories(db: Session = Depends(get_database)):
    categories = db.query(Category).all()
    return categories


@router.get("/{categoria_id}", response_model=CategoryBase)
def get_category(categoria_id: int, db: Session = Depends(get_database)):
    category = db.query(Category).filter(Category.id == categoria_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return category


@router.post("/", response_model=CategoryBase, status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryBase, db: Session = Depends(get_database)):
    existing = db.query(Category).filter(Category.nombre == payload.nombre).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A category with this name already exists"
        )

    new_category = Category(nombre=payload.nombre, descripcion=payload.descripcion)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(categoria_id: int, db: Session = Depends(get_database)):
    category = db.query(Category).filter(Category.id == categoria_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    db.delete(category)
    db.commit()
    return None
