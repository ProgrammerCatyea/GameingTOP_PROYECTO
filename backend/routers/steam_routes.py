import requests
from fastapi import APIRouter, HTTPException
from backend.core.config import settings

router = APIRouter(
    prefix="",
    tags=["Steam - Sincronización"]
)

@router.get("/top-games")
def get_top_steam_games():
    """
    Obtiene el top de juegos desde la API de Steam,
    usando la URL configurada en settings.STEAM_TOP_URL.
    """
    try:
        response = requests.get(settings.STEAM_TOP_URL, timeout=10)
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Error connecting to the Steam API"
            )

        data = response.json()
        games = data.get("response", {}).get("ranks", [])
        return {
            "total": len(games),
            "games": games[:25]
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal error: {str(e)}"
        )


@router.get("/details/{appid}")
def get_game_details(appid: int):
    """
    Obtiene los detalles de un juego específico de Steam por su AppID.

    Usa la misma plantilla de URL que tu servicio api_steam:
    settings.STEAM_APPDETAILS_URL debe tener algo como:
    'https://store.steampowered.com/api/appdetails?appids={appid}&l=spanish'
    """
    try:
        url = settings.STEAM_APPDETAILS_URL.format(appid=appid)
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Error retrieving game details from Steam API"
            )

        data = response.json()
        detalle = data.get(str(appid), {})

        if not detalle.get("success"):
            raise HTTPException(
                status_code=404,
                detail="Game not found in the Steam API"
            )

        game_info = detalle.get("data", {})

        return {
            "id": appid,
            "nombre": game_info.get("name"),
            "descripcion": game_info.get("short_description"),
            "generos": game_info.get("genres", []),
            "precio": game_info.get("price_overview", {}).get("final_formatted", "Gratis"),
            "desarrollador": game_info.get("developers", []),
            "editora": game_info.get("publishers", []),
            "imagen": game_info.get("header_image"),
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal error: {str(e)}"
        )
