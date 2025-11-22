from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.core.dependencies import get_database
from backend.models.ranking import Ranking
from backend.models.user import User
from backend.models.game import Game
from backend.models.associations import ranking_game
from backend.schemas.ranking_schema import (
    RankingDetail,
    RankingCreate,
    RankingUpdate,
)

router = APIRouter()


@router.get("/", response_model=List[RankingDetail])
def list_rankings(db: Session = Depends(get_database)):
    rankings = db.query(Ranking).all()
    return rankings


@router.get("/{ranking_id}", response_model=RankingDetail)
def get_ranking(ranking_id: int, db: Session = Depends(get_database)):
    ranking = db.query(Ranking).filter(Ranking.id == ranking_id).first()
    if not ranking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El ranking no existe.",
        )
    return ranking


@router.post("/", response_model=RankingDetail, status_code=status.HTTP_201_CREATED)
def create_ranking(payload: RankingCreate, db: Session = Depends(get_database)):
    user = None
    if payload.user_id is not None:
        user = db.query(User).filter(User.id == payload.user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El usuario asociado no existe.",
            )

    new_ranking = Ranking(
        nombre=payload.nombre,
        descripcion=payload.descripcion,
        tipo=payload.tipo,
        user=user,
    )

    db.add(new_ranking)
    db.commit()
    db.refresh(new_ranking)
    return new_ranking


@router.put("/{ranking_id}", response_model=RankingDetail)
def update_ranking(
    ranking_id: int,
    payload: RankingUpdate,
    db: Session = Depends(get_database),
):
    ranking = db.query(Ranking).filter(Ranking.id == ranking_id).first()
    if not ranking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El ranking no existe.",
        )

    if payload.nombre is not None:
        ranking.nombre = payload.nombre
    if payload.descripcion is not None:
        ranking.descripcion = payload.descripcion
    if payload.tipo is not None:
        ranking.tipo = payload.tipo
    if payload.user_id is not None:
        user = db.query(User).filter(User.id == payload.user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El usuario asociado no existe.",
            )
        ranking.user = user

    db.commit()
    db.refresh(ranking)
    return ranking


@router.post("/{ranking_id}/add_game/{juego_id}", response_model=RankingDetail)
def add_game_to_ranking(
    ranking_id: int,
    juego_id: int,
    posicion: Optional[int] = None,
    score: Optional[float] = None,
    db: Session = Depends(get_database),
):
    ranking = db.query(Ranking).filter(Ranking.id == ranking_id).first()
    game = db.query(Game).filter(Game.id == juego_id).first()

    if not ranking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El ranking no existe.",
        )
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El juego no existe.",
        )

    # Evitar duplicados
    if any(g.id == game.id for g in ranking.games):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El juego ya está asociado a este ranking.",
        )

    db.execute(
        ranking_game.insert().values(
            ranking_id=ranking.id,
            juego_id=game.id,
            posicion=posicion,
            score=score,
        )
    )

    db.commit()
    db.refresh(ranking)
    return ranking


@router.delete("/{ranking_id}/game/{juego_id}", response_model=RankingDetail)
def remove_game_from_ranking(
    ranking_id: int,
    juego_id: int,
    db: Session = Depends(get_database),
):
    ranking = db.query(Ranking).filter(Ranking.id == ranking_id).first()
    if not ranking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El ranking no existe.",
        )

    game = db.query(Game).filter(Game.id == juego_id).first()
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El juego no existe.",
        )

    db.execute(
        ranking_game.delete().where(
            (ranking_game.c.ranking_id == ranking_id)
            & (ranking_game.c.juego_id == juego_id)
        )
    )
    db.commit()
    db.refresh(ranking)
    return ranking


@router.delete("/{ranking_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ranking(ranking_id: int, db: Session = Depends(get_database)):
    ranking = db.query(Ranking).filter(Ranking.id == ranking_id).first()
    if not ranking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El ranking no existe.",
        )

    db.delete(ranking)
    db.commit()
    return None
