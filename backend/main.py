from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse   # ⬅️ IMPORTANTE
from backend.core.database import Base, engine
from backend.routers.game_routes import router as juegos_router
from backend.routers.category_routes import router as categorias_router
from backend.routers.ranking_routes import router as rankings_router
from backend.routers.user_routes import router as usuarios_router
from backend.routers.steam_routes import router as steam_router

app = FastAPI(
    title=" GameingTOP - Sistema de Gestión y Tendencias de Videojuegos",
    version="1.0.0",
    description="""
    Esta API permite gestionar y analizar información de videojuegos, jugadores, categorías y rankings
    sincronizados con Steam.
    """,
    contact={
        "name": "Nicolás Lozano Díaz",
        "email": "nicolas.lozano@ejemplo.com",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(juegos_router,    prefix="/juegos",    tags=["Juegos"])
app.include_router(categorias_router, prefix="/categorias", tags=["Categorías"])
app.include_router(rankings_router,  prefix="/rankings",  tags=["Rankings"])
app.include_router(usuarios_router,  prefix="/usuarios",  tags=["Usuarios"])
app.include_router(steam_router,     prefix="/steam",     tags=["Steam - Sincronización"])


FRONTEND_URL = "https://gameingtop-proyecto-1.onrender.com"

@app.get("/", include_in_schema=False)
def inicio():
    return RedirectResponse(url=FRONTEND_URL)

@app.get("/status", tags=["Estado del Servidor"])
def status():
    return {
        "status": "ok",
        "mensaje": "Backend GameingTOP operativo correctamente",
        "autor": "Nicolás Lozano Díaz",
        "version": "1.0.0"
    }
