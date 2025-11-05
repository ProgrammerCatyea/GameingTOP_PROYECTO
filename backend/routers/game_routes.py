from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.models.game import Juego
from backend.models.category import Categoria
from backend.schemas.game_schema import (
    JuegoBase,      
    JuegoDetail,     
    JuegoCreate,    
    JuegoUpdate      
)

router = APIRouter()


@router.get("/", response_model=List[JuegoDetail])
def listar_juegos(
    nombre: Optional[str] = Query(None, description="Filtra por nombre (contains)"),
    plataforma: Optional[str] = Query(None, description="Filtra por plataforma (contains)"),
    db: Session = Depends(get_db)
):
    q = db.query(Juego)
    if nombre:
        q = q.filter(Juego.nombre.ilike(f"%{nombre}%"))
    if plataforma:
        q = q.filter(Juego.plataforma.ilike(f"%{plataforma}%"))
    return q.all()


@router.get("/{juego_id}", response_model=JuegoDetail)
def obtener_juego(juego_id: int, db: Session = Depends(get_db)):
    juego = db.query(Juego).filter(Juego.id == juego_id).first()
    if not juego:
        raise HTTPException(status_code=404, detail="Juego no encontrado")
    return juego

@router.post("/", response_model=JuegoDetail, status_code=201)
def crear_juego(payload: JuegoCreate, db: Session = Depends(get_db)):
  
    nuevo = Juego(
        nombre=payload.nombre,
        plataforma=payload.plataforma,
        desarrollador=payload.desarrollador,
        genero_principal=payload.genero_principal,
    )

   
    if payload.categorias_ids:
        categorias = db.query(Categoria).filter(Categoria.id.in_(payload.categorias_ids)).all()
        if len(categorias) != len(set(payload.categorias_ids)):
            raise HTTPException(status_code=400, detail="Alguna categoría no existe")
        nuevo.categorias = categorias

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo



@router.put("/{juego_id}", response_model=JuegoDetail)
def actualizar_juego(juego_id: int, payload: JuegoUpdate, db: Session = Depends(get_db)):
    juego = db.query(Juego).filter(Juego.id == juego_id).first()
    if not juego:
        raise HTTPException(status_code=404, detail="Juego no encontrado")

    if payload.nombre is not None:
        juego.nombre = payload.nombre
    if payload.plataforma is not None:
        juego.plataforma = payload.plataforma
    if payload.desarrollador is not None:
        juego.desarrollador = payload.desarrollador
    if payload.genero_principal is not None:
        juego.genero_principal = payload.genero_principal

   
    if payload.categorias_ids is not None:
        if len(payload.categorias_ids) == 0:
            juego.categorias = []
        else:
            categorias = db.query(Categoria).filter(Categoria.id.in_(payload.categorias_ids)).all()
            if len(categorias) != len(set(payload.categorias_ids)):
                raise HTTPException(status_code=400, detail="Alguna categoría no existe")
            juego.categorias = categorias

    db.commit()
    db.refresh(juego)
    return juego


@router.delete("/{juego_id}", status_code=204)
def eliminar_juego(juego_id: int, db: Session = Depends(get_db)):
    juego = db.query(Juego).filter(Juego.id == juego_id).first()
    if not juego:
        raise HTTPException(status_code=404, detail="Juego no encontrado")
    db.delete(juego)
    db.commit()
    return
