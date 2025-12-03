from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    PROJECT_NAME: str = "GameingTOP API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = (
        "API para visualizar y analizar tendencias de videojuegos "
        "(Steam, Rankings, Categorías y Usuarios)."
    )

    DB_URL: str = ""

    def get_database_url(self):
        if self.DB_URL:
            return self.DB_URL
        BASE_DIR = Path(__file__).resolve().parents[2]
        DB_PATH = BASE_DIR / "data" / "gamingtop.db"
        return f"sqlite:///{DB_PATH}"

    ALLOWED_ORIGINS: List[str] = ["*"]

    STEAM_API_KEY: str = ""
    STEAM_TOP_URL: str = (
        "https://api.steampowered.com/ISteamChartsService/GetMostPlayedGames/v1/"
    )
    STEAM_APPDETAILS_URL: str = (
        "https://store.steampowered.com/api/appdetails?appids={appid}"
    )

    class Config:
        env_file = ".env"


settings = Settings()
