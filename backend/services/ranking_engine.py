from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.services.api_steam import sincronizar_juegos_steam

router = APIRouter()

@router.post("/sync", tags=["Steam"])
def sincronizar_steam(db: Session = Depends(get_db)):
    juegos_nuevos = sincronizar_juegos_steam(db)
    return {
        "status": " Sincronización completada",
        "nuevos_registros": len(juegos_nuevos),
        "mensaje": "Base de datos actualizada con los juegos más populares de Steam."
    }
