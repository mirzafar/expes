from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки приложения. Читаются из переменных окружения / файла .env."""

    # Application
    app_name: str = "Expes API"
    debug: bool = True

    # MongoDB
    mongo_uri: str = "mongodb://localhost:27017"
    mongo_db: str = "expes"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # JWT / Security
    jwt_secret: str = "change-me-please-generate-a-real-secret"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # CORS — список адресов фронтенда через запятую
    cors_origins: str = "http://localhost:5173"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


# Единственный экземпляр настроек на всё приложение
settings = Settings()
