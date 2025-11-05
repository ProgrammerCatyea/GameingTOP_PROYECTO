import os
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):

    PROJECT_NAME: str = "GameingTOP API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = (
        "API para visualizar y analizar tendencias de videojuegos "
        "(Steam, Rankings, Categorías, Jugadores)."
    )


    DB_URL: str = "sqlite:///./backend/data/gamingtop.db"

   
    ALLOWED_ORIGINS: List[str] = ["*"]  

    STEAM_API_KEY: str = os.getenv("STEAM_API_KEY", "")
    STEAM_TOP_URL: str = (
        "https://api.steampowered.com/ISteamChartsService/GetMostPlayedGames/v1/"
    )
    STEAM_APPDETAILS_URL: str = (
        "https://store.steampowered.com/api/appdetails?appids={appid}"
    )

    class Config:
        env_file = ".env"  



settings = Settings()
