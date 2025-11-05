from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.core.dependencies import get_database
from backend.models.ranking import Ranking
from backend.models.user import Usuario
from backend.models.game import Juego
from backend.models.associations import ranking_juego
from backend.schemas.ranking_schema import RankingBase, RankingDetail

router = APIRouter(
    prefix="/api/v1/rankings",
    tags=["Rankings"]
)

@router.get("/", response_model=List[RankingDetail])
def listar_rankings(db: Session = Depends(get_database)):
    return db.query(Ranking).all()

@router.get("/{ranking_id}", response_model=RankingDetail)
def obtener_ranking(ranking_id: int, db: Session = Depends(get_database)):
    ranking = db.query(Ranking).filter(Ranking.id == ranking_id).first()
    if not ranking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ranking no encontrado"
        )
    return ranking

@router.post("/", response_model=RankingDetail, status_code=status.HTTP_201_CREATED)
def crear_ranking(payload: RankingBase, db: Session = Depends(get_database)):
    usuario = None
    if payload.id:
        usuario = db.query(Usuario).filter(Usuario.id == payload.id).first()
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )

    nuevo = Ranking(
        nombre=payload.nombre,
        descripcion=payload.descripcion,
        tipo=payload.tipo,
        usuario=usuario
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.post("/{ranking_id}/add_game/{juego_id}", response_model=RankingDetail)
def agregar_juego_a_ranking(
    ranking_id: int,
    juego_id: int,
    posicion: Optional[int] = None,
    score: Optional[float] = None,
    nota: Optional[str] = None,
    db: Session = Depends(get_database)
):
    ranking = db.query(Ranking).filter(Ranking.id == ranking_id).first()
    juego = db.query(Juego).filter(Juego.id == juego_id).first()

    if not ranking:
        raise HTTPException(status_code=404, detail="Ranking no encontrado")
    if not juego:
        raise HTTPException(status_code=404, detail="Juego no encontrado")

    if any(j.id == juego.id for j in ranking.juegos):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El juego ya está en este ranking"
        )

    db.execute(
        ranking_juego.insert().values(
            ranking_id=ranking.id,
            juego_id=juego.id,
            posicion=posicion,
            score=score,
            nota=nota
        )
    )

    db.commit()
    db.refresh(ranking)
    return ranking

@router.delete("/{ranking_id}/game/{juego_id}", response_model=RankingDetail)
def eliminar_juego_de_ranking(ranking_id: int, juego_id: int, db: Session = Depends(get_database)):
    ranking = db.query(Ranking).filter(Ranking.id == ranking_id).first()
    if not ranking:
        raise HTTPException(status_code=404, detail="Ranking no encontrado")

    juego = db.query(Juego).filter(Juego.id == juego_id).first()
    if not juego:
        raise HTTPException(status_code=404, detail="Juego no encontrado")

    db.execute(
        ranking_juego.delete().where(
            (ranking_juego.c.ranking_id == ranking_id)
            & (ranking_juego.c.juego_id == juego_id)
        )
    )
    db.commit()
    db.refresh(ranking)
    return ranking

@router.delete("/{ranking_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_ranking(ranking_id: int, db: Session = Depends(get_database)):
    ranking = db.query(Ranking).filter(Ranking.id == ranking_id).first()
    if not ranking:
        raise HTTPException(status_code=404, detail="Ranking no encontrado")

    db.delete(ranking)
    db.commit()
    return None
