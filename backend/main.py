from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.core.database import Base, engine

# Routers
from backend.routers.game_routes import router as games_router
from backend.routers.category_routes import router as categories_router
from backend.routers.ranking_routes import router as rankings_router
from backend.routers.user_routes import router as users_router
from backend.routers.steam_routes import router as steam_router

app = FastAPI(
    title="GameingTOP - Video Game Analytics & Ranking System",
    version="1.0.0",
    description="""
    API for managing and analyzing video game trends, users, categories, and rankings,
    with real-time Steam synchronization.

    Developer: **Nicolás Lozano Díaz**  
    Technologies: FastAPI · SQLAlchemy · SQLite · Pydantic  
    Objective: Manage, relate and visualize the most popular video games.
    """,
    contact={
        "name": "Nicolás Lozano Díaz",
        "email": "nicolas.lozano@ejemplo.com",
    },
)

# -------------------------------------------------------
# CORS
# -------------------------------------------------------
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

@app.get("/", tags=["Server"])
def home():
    return {
        "status": "ok",
        "message": "GameingTOP Backend Running Successfully",
        "author": "Nicolás Lozano Díaz",
        "version": "1.0.0"
    }
