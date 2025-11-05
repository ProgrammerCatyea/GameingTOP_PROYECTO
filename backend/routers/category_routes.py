from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.core.dependencies import get_database
from backend.models.category import Categoria
from backend.schemas.category_schema import CategoriaBase

router = APIRouter(
    prefix="/api/v1/categories",
    tags=["Categories"]
)


@router.get("/", response_model=List[CategoriaBase])
def listar_categorias(db: Session = Depends(get_database)):
    categorias = db.query(Categoria).all()
    return categorias


@router.get("/{categoria_id}", response_model=CategoriaBase)
def obtener_categoria(categoria_id: int, db: Session = Depends(get_database)):
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )
    return categoria


@router.post("/", response_model=CategoriaBase, status_code=status.HTTP_201_CREATED)
def crear_categoria(payload: CategoriaBase, db: Session = Depends(get_database)):
    existe = db.query(Categoria).filter(Categoria.nombre == payload.nombre).first()
    if existe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una categoría con ese nombre"
        )

    nueva = Categoria(nombre=payload.nombre, descripcion=payload.descripcion)
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_categoria(categoria_id: int, db: Session = Depends(get_database)):
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )

    db.delete(categoria)
    db.commit()
    return None
