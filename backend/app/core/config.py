"""Configuración de la aplicación, leída desde el archivo .env.

Si falta una variable obligatoria, la aplicación no arranca y muestra
qué variable falta (principio "fail fast").
"""

from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

# backend/app/core/config.py -> la raíz del repositorio está tres niveles arriba
RAIZ_PROYECTO = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=RAIZ_PROYECTO / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Base de datos
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str
    db_user: str
    db_password: SecretStr

    # Autenticación (JWT)
    jwt_secret_key: SecretStr
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Frontend autorizado (CORS)
    frontend_origin: str = "http://localhost:5173"


settings = Settings()