from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from backend.core.database import get_db
from backend.models.ranking import Ranking
from backend.models.user import Usuario
from backend.models.game import Juego
from backend.models.associations import ranking_juego
from backend.schemas.ranking_schema import RankingBase, RankingDetail

router = APIRouter()

@router.get("/", response_model=List[RankingDetail])
def listar_rankings(db: Session = Depends(get_db)):
    return db.query(Ranking).all()

@router.get("/{ranking_id}", response_model=RankingDetail)
def obtener_ranking(ranking_id: int, db: Session = Depends(get_db)):
    ranking = db.query(Ranking).filter(Ranking.id == ranking_id).first()
    if not ranking:
        raise HTTPException(status_code=404, detail="Ranking no encontrado")
    return ranking

@router.post("/", response_model=RankingDetail, status_code=201)
def crear_ranking(payload: RankingBase, db: Session = Depends(get_db)):
 
    usuario = None
    if payload.id:
        usuario = db.query(Usuario).filter(Usuario.id == payload.id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

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


@router.post("/{ranking_id}/agregar_juego/{juego_id}", response_model=RankingDetail)
def agregar_juego_a_ranking(
    ranking_id: int,
    juego_id: int,
    posicion: Optional[int] = None,
    score: Optional[float] = None,
    nota: Optional[str] = None,
    db: Session = Depends(get_db)
):
    ranking = db.query(Ranking).filter(Ranking.id == ranking_id).first()
    juego = db.query(Juego).filter(Juego.id == juego_id).first()

    if not ranking:
        raise HTTPException(status_code=404, detail="Ranking no encontrado")
    if not juego:
        raise HTTPException(status_code=404, detail="Juego no encontrado")

    for j in ranking.juegos:
        if j.id == juego.id:
            raise HTTPException(status_code=400, detail="El juego ya está en este ranking")

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

@router.delete("/{ranking_id}/juego/{juego_id}", response_model=RankingDetail)
def eliminar_juego_de_ranking(ranking_id: int, juego_id: int, db: Session = Depends(get_db)):
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

@router.delete("/{ranking_id}", status_code=204)
def eliminar_ranking(ranking_id: int, db: Session = Depends(get_db)):
    ranking = db.query(Ranking).filter(Ranking.id == ranking_id).first()
    if not ranking:
        raise HTTPException(status_code=404, detail="Ranking no encontrado")

    db.delete(ranking)
    db.commit()
    return
