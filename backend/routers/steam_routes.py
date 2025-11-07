import requests
from fastapi import APIRouter, HTTPException
from backend.core.config import settings

router = APIRouter(
    prefix="/api/v1/steam",
    tags=["Steam"]
)


@router.get("/top-games")
def get_top_steam_games():
    try:
        response = requests.get(settings.STEAM_TOP_URL)
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

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal error: {str(e)}"
        )


@router.get("/details/{appid}")
def get_game_details(appid: int):
    try:
        url = settings.STEAM_APPDETAILS_URL.format(appids=appid)
        response = requests.get(url)

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Error retrieving game details from Steam API"
            )

        data = response.json()
        game_info = data.get(str(appid), {}).get("data", {})

        if not game_info:
            raise HTTPException(
                status_code=404,
                detail="Game not found in the Steam API"
            )

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

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal error: {str(e)}"
        )
