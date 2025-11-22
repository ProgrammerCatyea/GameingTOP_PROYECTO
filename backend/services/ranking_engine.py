from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.core.dependencies import get_database
from backend.services.api_steam import sincronizar_juegos_steam

router = APIRouter(
    prefix="/api/v1/steam",
    tags=["Steam"]
)

@router.post("/sync", status_code=status.HTTP_200_OK)
def sincronizar_steam(db: Session = Depends(get_database)):
    juegos_nuevos = sincronizar_juegos_steam(db)

    return {
        "status": "ok",
        "nuevos_registros": len(juegos_nuevos),
        "mensaje": "Base de datos actualizada con los juegos más populares de Steam."
    }

