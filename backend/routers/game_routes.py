from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from backend.core.dependencies import get_database
from backend.models.game import Juego
from backend.models.category import Categoria
from backend.schemas.game_schema import JuegoBase, JuegoDetail, JuegoCreate, JuegoUpdate

router = APIRouter(
    prefix="/api/v1/games",
    tags=["Games"]
)


@router.get("/", response_model=List[JuegoDetail])
def listar_juegos(
    nombre: Optional[str] = Query(None, description="Filtra por nombre (contains)"),
    plataforma: Optional[str] = Query(None, description="Filtra por plataforma (contains)"),
    db: Session = Depends(get_database)
):
    q = db.query(Juego)
    if nombre:
        q = q.filter(Juego.nombre.ilike(f"%{nombre}%"))
    if plataforma:
        q = q.filter(Juego.plataforma.ilike(f"%{plataforma}%"))
    return q.all()

@router.get("/{juego_id}", response_model=JuegoDetail)
def obtener_juego(juego_id: int, db: Session = Depends(get_database)):
    juego = db.query(Juego).filter(Juego.id == juego_id).first()
    if not juego:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Juego no encontrado"
        )
    return juego


@router.post("/", response_model=JuegoDetail, status_code=status.HTTP_201_CREATED)
def crear_juego(payload: JuegoCreate, db: Session = Depends(get_database)):
    nuevo = Juego(
        nombre=payload.nombre,
        plataforma=payload.plataforma,
        desarrollador=payload.desarrollador,
        genero_principal=payload.genero_principal,
    )

    if payload.categorias_ids:
        categorias = db.query(Categoria).filter(Categoria.id.in_(payload.categorias_ids)).all()
        if len(categorias) != len(set(payload.categorias_ids)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Alguna categoría no existe"
            )
        nuevo.categorias = categorias

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.put("/{juego_id}", response_model=JuegoDetail)
def actualizar_juego(juego_id: int, payload: JuegoUpdate, db: Session = Depends(get_database)):
    juego = db.query(Juego).filter(Juego.id == juego_id).first()
    if not juego:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Juego no encontrado"
        )
    for campo, valor in payload.dict(exclude_unset=True).items():
        if hasattr(juego, campo):
            setattr(juego, campo, valor)

    if payload.categorias_ids is not None:
        if len(payload.categorias_ids) == 0:
            juego.categorias = []
        else:
            categorias = db.query(Categoria).filter(Categoria.id.in_(payload.categorias_ids)).all()
            if len(categorias) != len(set(payload.categorias_ids)):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Alguna categoría no existe"
                )
            juego.categorias = categorias

    db.commit()
    db.refresh(juego)
    return juego


@router.delete("/{juego_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_juego(juego_id: int, db: Session = Depends(get_database)):
    juego = db.query(Juego).filter(Juego.id == juego_id).first()
    if not juego:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Juego no encontrado"
        )
    db.delete(juego)
    db.commit()
    return None
