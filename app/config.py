from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "API CRUD avec Authentification"
    database_url: str

    class Config:
        env_file = ".env"

# Initialisation des paramètres
settings = Settings()
