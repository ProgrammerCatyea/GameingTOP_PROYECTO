import requests
from typing import List, Optional
from sqlalchemy.orm import Session
from backend.core.config import settings
from backend.models.game import Game


def obtener_top_steam(limit: int = 25) -> List[dict]:
   
    try:
        response = requests.get(settings.STEAM_TOP_URL, timeout=10)
        response.raise_for_status()

        data = response.json()
        juegos = data.get("response", {}).get("ranks", [])
        return juegos[:limit]

    except requests.RequestException as e:
        print(f"[STEAM][ERROR TOP] No se pudo obtener el top: {e}")
        return []
    except Exception as e:
        print(f"[STEAM][ERROR DESCONOCIDO TOP] {e}")
        return []


def obtener_detalle_juego(appid: int) -> Optional[dict]:
  
    try:
        url = settings.STEAM_APPDETAILS_URL.format(appid=appid)
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()

        data = resp.json()
        detalle = data.get(str(appid), {})

        if not detalle.get("success"):
            print(f"[STEAM][AVISO] No se encontraron datos para appid {appid}")
            return None

        info = detalle.get("data", {})

        return {
            "nombre": info.get("name"),
            "desarrollador": ", ".join(info.get("developers", []))
            if info.get("developers")
            else None,
            "genero_principal": (
                info.get("genres", [{}])[0].get("description")
                if info.get("genres")
                else None
            ),
        }

    except requests.RequestException as e:
        print(f"[STEAM][ERROR DETALLE] appid={appid}: {e}")
        return None
    except Exception as e:
        print(f"[STEAM][ERROR DESCONOCIDO DETALLE {appid}] {e}")
        return None


def sincronizar_juegos_steam(db: Session, limit: int = 25) -> List[Game]:
    top = obtener_top_steam(limit)
    if not top:
        print("[STEAM][AVISO] No se encontraron juegos para sincronizar.")
        return []

    sincronizados: List[Game] = []

    for entry in top:
        appid = entry.get("appid")
        if not appid:
            continue

        detalle = obtener_detalle_juego(appid)
        if not detalle:
            continue

        juego_existente = db.query(Game).filter(Game.appid == appid).first()

        if juego_existente:
            juego_existente.nombre = detalle["nombre"]
            juego_existente.desarrollador = detalle["desarrollador"]
            juego_existente.genero_principal = detalle["genero_principal"]
            print(f"[STEAM][ACTUALIZADO] {detalle['nombre']}")
        else:
            nuevo = Game(
                appid=appid,
                nombre=detalle["nombre"],
                plataforma="Steam/PC",
                desarrollador=detalle["desarrollador"],
                genero_principal=detalle["genero_principal"],
            )
            db.add(nuevo)
            sincronizados.append(nuevo)
            print(f"[STEAM][AGREGADO] {detalle['nombre']}")

    db.commit()
    return sincronizados
