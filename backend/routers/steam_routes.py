import requests
from fastapi import APIRouter, HTTPException
from backend.core.config import settings

router = APIRouter(
    prefix="/api/v1/steam",
    tags=["Steam"]
)

@router.get("/top-games")
def obtener_top_steam_games():
    try:
        response = requests.get(settings.STEAM_TOP_URL)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error al conectar con Steam API")

        data = response.json()
        juegos = data.get("response", {}).get("ranks", [])
        return {
            "total": len(juegos),
            "games": juegos[:25]  
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get("/details/{appid}")
def obtener_detalles_juego(appid: int):
    try:
        url = settings.STEAM_APPDETAILS_URL.format(appids=appid)
        response = requests.get(url)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error al obtener detalles del juego")

        data = response.json()
        juego_info = data.get(str(appid), {}).get("data", {})

        if not juego_info:
            raise HTTPException(status_code=404, detail="Juego no encontrado en la API de Steam")

        return {
            "id": appid,
            "nombre": juego_info.get("name"),
            "descripcion": juego_info.get("short_description"),
            "generos": juego_info.get("genres", []),
            "precio": juego_info.get("price_overview", {}).get("final_formatted", "Gratis"),
            "desarrollador": juego_info.get("developers", []),
            "editora": juego_info.get("publishers", []),
            "imagen": juego_info.get("header_image"),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
