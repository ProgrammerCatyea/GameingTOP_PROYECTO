import requests
from fastapi import APIRouter, HTTPException
from backend.core.config import settings

router = APIRouter()


@router.get("/top", tags=["Steam"])
def get_top_steam_games(limit: int = 25):
    try:
        response = requests.get(settings.STEAM_TOP_URL)

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Error al conectarse con la API de Steam."
            )

        data = response.json()
        ranks = data.get("response", {}).get("ranks", [])

        return {
            "estado": "ok",
            "total_encontrados": len(ranks),
            "limite": limit,
            "juegos": ranks[:limit],
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno al consultar Steam: {str(e)}"
        )


@router.get("/details/{appid}", tags=["Steam"])
def get_game_details(appid: int):
    try:
        url = settings.STEAM_APPDETAILS_URL.format(appid=appid)
        response = requests.get(url)

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Error al obtener detalles del juego desde Steam."
            )

        data = response.json()
        info = data.get(str(appid), {})

        if not info.get("success", False):
            raise HTTPException(
                status_code=404,
                detail="El juego no existe en Steam."
            )

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
        raise HTTPException(
            status_code=500,
            detail=f"Error interno: {str(e)}"
        )
