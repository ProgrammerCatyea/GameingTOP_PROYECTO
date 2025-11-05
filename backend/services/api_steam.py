import requests
from sqlalchemy.orm import Session
from backend.models.game import Juego


STEAM_TOP_URL = "https://api.steampowered.com/ISteamChartsService/GetMostPlayedGames/v1/"


STEAM_APPDETAILS_URL = "https://store.steampowered.com/api/appdetails?appids={appid}"


def obtener_top_steam(limit: int = 25):
    try:
        response = requests.get(STEAM_TOP_URL)
        response.raise_for_status()
        data = response.json()
        juegos = data["response"]["ranks"][:limit]
        return juegos
    except Exception as e:
        print(f"Error al obtener top Steam: {e}")
        return []


def obtener_detalle_juego(appid: int):
    try:
        resp = requests.get(STEAM_APPDETAILS_URL.format(appid=appid))
        resp.raise_for_status()
        data = resp.json()
        detalle = data.get(str(appid), {})
        if not detalle.get("success"):
            return None
        info = detalle["data"]
        return {
            "nombre": info.get("name"),
            "desarrollador": ", ".join(info.get("developers", [])) if info.get("developers") else None,
            "genero_principal": info.get("genres", [{}])[0].get("description") if info.get("genres") else None,
        }
    except Exception as e:
        print(f"Error al obtener detalles de appid {appid}: {e}")
        return None


def sincronizar_juegos_steam(db: Session, limit: int = 25):
    top = obtener_top_steam(limit)
    sincronizados = []

    for entry in top:
        appid = entry.get("appid")
        detalle = obtener_detalle_juego(appid)
        if not detalle:
            continue

        juego_existente = db.query(Juego).filter(Juego.appid == appid).first()

        if juego_existente:
            juego_existente.nombre = detalle["nombre"]
            juego_existente.desarrollador = detalle["desarrollador"]
            juego_existente.genero_principal = detalle["genero_principal"]
        else:
            nuevo = Juego(
                appid=appid,
                nombre=detalle["nombre"],
                plataforma="Steam/PC",
                desarrollador=detalle["desarrollador"],
                genero_principal=detalle["genero_principal"],
            )
            db.add(nuevo)
            sincronizados.append(nuevo)

    db.commit()
    return sincronizados
