from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.core.database import get_db
from backend.models.category import Categoria
from backend.schemas.category_schema import CategoriaBase

router = APIRouter()

@router.get("/", response_model=List[CategoriaBase])
def listar_categorias(db: Session = Depends(get_db)):
    return db.query(Categoria).all()


@router.get("/{categoria_id}", response_model=CategoriaBase)
def obtener_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria


@router.post("/", response_model=CategoriaBase, status_code=201)
def crear_categoria(payload: CategoriaBase, db: Session = Depends(get_db)):
    existe = db.query(Categoria).filter(Categoria.nombre == payload.nombre).first()
    if existe:
        raise HTTPException(status_code=400, detail="Ya existe una categoría con ese nombre")

    nueva = Categoria(nombre=payload.nombre, descripcion=payload.descripcion)
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


@router.delete("/{categoria_id}", status_code=204)
def eliminar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    db.delete(categoria)
    db.commit()
    return
