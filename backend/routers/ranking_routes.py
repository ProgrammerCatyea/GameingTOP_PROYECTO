from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.core.dependencies import get_database
from backend.models.ranking import Ranking
from backend.models.user import User
from backend.models.game import Game
from backend.models.associations import ranking_game
from backend.schemas.ranking_schema import RankingBase, RankingDetail

router = APIRouter(
    prefix="",
    tags=["Rankings"]
)


@router.get("/", response_model=List[RankingDetail])
def list_rankings(db: Session = Depends(get_database)):
    return db.query(Ranking).all()


@router.get("/{ranking_id}", response_model=RankingDetail)
def get_ranking(ranking_id: int, db: Session = Depends(get_database)):
    ranking = db.query(Ranking).filter(Ranking.id == ranking_id).first()
    if not ranking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ranking not found"
        )
    return ranking


@router.post("/", response_model=RankingDetail, status_code=status.HTTP_201_CREATED)
def create_ranking(payload: RankingBase, db: Session = Depends(get_database)):
    user = None
    if payload.id:
        user = db.query(User).filter(User.id == payload.id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

    new_ranking = Ranking(
        nombre=payload.nombre,
        descripcion=payload.descripcion,
        tipo=payload.tipo,
        user=user
    )

    db.add(new_ranking)
    db.commit()
    db.refresh(new_ranking)
    return new_ranking


@router.post("/{ranking_id}/add_game/{juego_id}", response_model=RankingDetail)
def add_game_to_ranking(
    ranking_id: int,
    juego_id: int,
    posicion: Optional[int] = None,
    score: Optional[float] = None,
    nota: Optional[str] = None,
    db: Session = Depends(get_database)
):
    ranking = db.query(Ranking).filter(Ranking.id == ranking_id).first()
    game = db.query(Game).filter(Game.id == juego_id).first()

    if not ranking:
        raise HTTPException(status_code=404, detail="Ranking not found")
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    if any(g.id == game.id for g in ranking.games):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The game is already in this ranking"
        )

    db.execute(
        ranking_game.insert().values(
            ranking_id=ranking.id,
            juego_id=game.id,
            posicion=posicion,
            score=score,
            nota=nota
        )
    )

    db.commit()
    db.refresh(ranking)
    return ranking


@router.delete("/{ranking_id}/game/{juego_id}", response_model=RankingDetail)
def remove_game_from_ranking(ranking_id: int, juego_id: int, db: Session = Depends(get_database)):
    ranking = db.query(Ranking).filter(Ranking.id == ranking_id).first()
    if not ranking:
        raise HTTPException(status_code=404, detail="Ranking not found")

    game = db.query(Game).filter(Game.id == juego_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

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
        raise HTTPException(status_code=404, detail="Ranking not found")

    db.delete(ranking)
    db.commit()
    return None
