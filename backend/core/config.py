from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",   
    )

    env: str = "development"              
    app_name: str = "GameingTOP"
    port: int = 8000


    database_url: str = "sqlite:///./app.db"

   
    supabase_url: str | None = None
    supabase_anon_key: str | None = None
    supabase_service_role_key: str | None = None
    supabase_bucket_name: str | None = "rankings-images"

    frontend_origin: str = "http://localhost:5500"



settings = Settings()
