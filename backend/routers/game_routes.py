from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from backend.core.dependencies import get_database
from backend.models.game import Game
from backend.models.category import Category
from backend.schemas.game_schema import GameBase, GameDetail, GameCreate, GameUpdate

router = APIRouter(
    prefix="",
    tags=["Juegos"]
)


@router.get("/", response_model=List[GameDetail])
def list_games(
    nombre: Optional[str] = Query(None, description="Filter by name (contains)"),
    plataforma: Optional[str] = Query(None, description="Filter by platform (contains)"),
    db: Session = Depends(get_database)
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
            detail="Game not found"
        )
    return game


@router.post("/", response_model=GameDetail, status_code=status.HTTP_201_CREATED)
def create_game(payload: GameCreate, db: Session = Depends(get_database)):
    new_game = Game(
        nombre=payload.nombre,
        plataforma=payload.plataforma,
        desarrollador=payload.desarrollador,
        genero_principal=payload.genero_principal,
    )

    if payload.categorias_ids:
        categories = db.query(Category).filter(Category.id.in_(payload.categorias_ids)).all()
        if len(categories) != len(set(payload.categorias_ids)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="One or more categories do not exist"
            )
        new_game.categories = categories

    db.add(new_game)
    db.commit()
    db.refresh(new_game)
    return new_game


@router.put("/{juego_id}", response_model=GameDetail)
def update_game(juego_id: int, payload: GameUpdate, db: Session = Depends(get_database)):
    game = db.query(Game).filter(Game.id == juego_id).first()
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )

    for field, value in payload.dict(exclude_unset=True).items():
        if hasattr(game, field):
            setattr(game, field, value)

    if payload.categorias_ids is not None:
        if len(payload.categorias_ids) == 0:
            game.categories = []
        else:
            categories = db.query(Category).filter(Category.id.in_(payload.categorias_ids)).all()
            if len(categories) != len(set(payload.categorias_ids)):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="One or more categories do not exist"
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
            detail="Game not found"
        )
    db.delete(game)
    db.commit()
    return None
