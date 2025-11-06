from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.core.database import Base, engine
from backend.routers.game_routes import router as games_router
from backend.routers.category_routes import router as categories_router
from backend.routers.ranking_routes import router as rankings_router
from backend.routers.user_routes import router as users_router
from backend.routers.steam_routes import router as steam_router

app = FastAPI(
    title="GameingTOP API",
    version="1.0.0",
    description="API para visualizar y gestionar tendencias de videojuegos en Steam y rankings personalizados.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)

app.include_router(games_router, prefix="/api/v1/games", tags=["Games"])
app.include_router(categories_router, prefix="/api/v1/categories", tags=["Categories"])
app.include_router(rankings_router, prefix="/api/v1/rankings", tags=["Rankings"])
app.include_router(users_router, prefix="/api/v1/users", tags=["Users"])
app.include_router(steam_router, prefix="/api/v1/steam", tags=["Steam"])

@app.get("/health", tags=["Status"])
def healthcheck():
    return {
        "status": "ok",
        "mensaje": "✅ Backend de GameingTOP funcionando correctamente",
    }
