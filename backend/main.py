from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.core.database import Base, engine
from backend.routers.game_routes import router as juegos_router
from backend.routers.category_routes import router as categorias_router
from backend.routers.ranking_routes import router as rankings_router
from backend.routers.user_routes import router as usuarios_router
from backend.routers.steam_routes import router as steam_router

app = FastAPI(
    title="GameingTOP API",
    version="1.0.0",
    description="API para visualizar y analizar tendencias de videojuegos en Steam."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(juegos_router, prefix="/api/v1/juegos", tags=[" Juegos"])
app.include_router(categorias_router, prefix="/api/v1/categorias", tags=[" Categorías"])
app.include_router(rankings_router, prefix="/api/v1/rankings", tags=[" Rankings"])
app.include_router(usuarios_router, prefix="/api/v1/usuarios", tags=[" Usuarios"])
app.include_router(steam_router, prefix="/api/v1/steam", tags=[" Steam"])

@app.get("/estado", tags=["Estado"])
def healthcheck():
    return {"status": "ok", "mensaje": "Backend de GameingTOP funcionando correctamente"}
