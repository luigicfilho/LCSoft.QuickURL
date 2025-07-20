from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    shorturl_max_retries: int = 3
    default_expiration_days: int = 30
    database_url: str = "sqlite://db.sqlite3"
    jwt_secret: str = "supersecretadmin"
    admin_list_urls_limit: str = "5/minute"
    admin_delete_url_limit: str = "5/minute"
    admin_stats_limit: str = "10/minute"
    shorturl_default_limit: str = "5/minute"
    env: str = "development"
    cors_allowed_origins: list[str] = []

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
