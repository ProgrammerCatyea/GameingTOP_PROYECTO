from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from backend.core.dependencies import get_database
from backend.services.api_steam import sincronizar_juegos_steam
from backend.core.config import settings
import requests

router = APIRouter()


@router.post("/sync", status_code=status.HTTP_200_OK, tags=["Steam"])
def sincronizar_steam(db: Session = Depends(get_database)):
    """
    Sincroniza los juegos más jugados de Steam con la base de datos local.
    """
    juegos_nuevos = sincronizar_juegos_steam(db)
    return {
        "status": "ok",
        "nuevos_registros": len(juegos_nuevos),
        "mensaje": "Base de datos actualizada con los juegos más populares de Steam.",
    }


@router.get("/top", tags=["Steam"])
def get_top_steam(limit: int = 25):
    """
    Consulta el top de juegos más jugados en Steam (sin guardar en la BD).
    """
    try:
        resp = requests.get(settings.STEAM_TOP_URL, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        ranks = data.get("response", {}).get("ranks", [])
        return {
            "estado": "ok",
            "limite": limit,
            "total_encontrados": len(ranks),
            "juegos": ranks[:limit],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar Steam: {e}")


@router.get("/details/{appid}", tags=["Steam"])
def get_steam_game_details(appid: int):
    """
    Consulta información detallada de un juego en Steam por su appid.
    """
    try:
        url = settings.STEAM_APPDETAILS_URL.format(appid=appid)
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()

        data = resp.json()
        info = data.get(str(appid), {})

        if not info.get("success", False):
            raise HTTPException(status_code=404, detail="El juego no existe en Steam.")

        datos = info.get("data", {})

        return {
            "appid": appid,
            "nombre": datos.get("name"),
            "descripcion": datos.get("short_description"),
            "generos": datos.get("genres", []),
            "precio": datos.get("price_overview", {}).get("final_formatted", "Gratis"),
            "desarrollador": datos.get("developers", []),
            "editora": datos.get("publishers", []),
            "imagen": datos.get("header_image"),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener detalles: {e}")
