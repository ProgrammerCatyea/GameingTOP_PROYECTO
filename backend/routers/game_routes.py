from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.core.dependencies import get_database
from backend.models.game import Game
from backend.models.category import Category
from backend.models.user import User
from backend.schemas.game_schema import GameDetail, GameCreate, GameUpdate

router = APIRouter()


@router.get("/", response_model=List[GameDetail])
def list_games(
    nombre: Optional[str] = Query(None, description="Filtrar por nombre (contiene)"),
    plataforma: Optional[str] = Query(None, description="Filtrar por plataforma (contiene)"),
    db: Session = Depends(get_database),
):
    query = db.query(Game)
    if nombre:
        query = query.filter(Game.nombre.ilike(f"%{nombre}%"))
    if plataforma:
        query = query.filter(Game.plataforma.ilike(f"%{plataforma}%"))
    return query.all()



@router.get("/{juego_id}", response_model=GameDetail)
def get_game(juego_id: int, db: Session = Depends(get_database)):
    game = db.query(Game).filter(Game.id == juego_id).first()
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El juego no existe.",
        )
    return game



@router.post("/", response_model=GameDetail, status_code=status.HTTP_201_CREATED)
def create_game(payload: GameCreate, db: Session = Depends(get_database)):
   
    user = None
    if payload.user_id is not None:
        user = db.query(User).filter(User.id == payload.user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El usuario asociado no existe.",
            )

    new_game = Game(
        nombre=payload.nombre,
        plataforma=payload.plataforma,
        desarrollador=payload.desarrollador,
        genero_principal=payload.genero_principal,
        user=user,
    )

 
    if payload.categorias_ids:
        categories = db.query(Category).filter(
            Category.id.in_(payload.categorias_ids)
        ).all()
        if len(categories) != len(set(payload.categorias_ids)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Una o más categorías no existen.",
            )
        new_game.categories = categories

    db.add(new_game)
    db.commit()
    db.refresh(new_game)
    return new_game



@router.put("/{juego_id}", response_model=GameDetail)
def update_game(
    juego_id: int,
    payload: GameUpdate,
    db: Session = Depends(get_database),
):
    game = db.query(Game).filter(Game.id == juego_id).first()
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El juego no existe.",
        )
    if payload.nombre is not None:
        game.nombre = payload.nombre
    if payload.plataforma is not None:
        game.plataforma = payload.plataforma
    if payload.desarrollador is not None:
        game.desarrollador = payload.desarrollador
    if payload.genero_principal is not None:
        game.genero_principal = payload.genero_principal
    if payload.user_id is not None:
        user = db.query(User).filter(User.id == payload.user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El usuario asociado no existe.",
            )
        game.user = user

  
    if payload.categorias_ids is not None:
        if len(payload.categorias_ids) == 0:
            game.categories = []
        else:
            categories = db.query(Category).filter(
                Category.id.in_(payload.categorias_ids)
            ).all()
            if len(categories) != len(set(payload.categorias_ids)):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Una o más categorías no existen.",
                )
            game.categories = categories

    db.commit()
    db.refresh(game)
    return game

@router.delete("/{juego_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_game(juego_id: int, db: Session = Depends(get_database)):
    game = db.query(Game).filter(Game.id == juego_id).first()
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El juego no existe.",
        )
    db.delete(game)
    db.commit()
    return None
