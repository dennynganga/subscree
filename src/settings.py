from pydantic import BaseSettings, PostgresDsn, RedisDsn


class Settings(BaseSettings):
    # DB
    database_url: PostgresDsn = "postgresql://subscree:subscree@127.0.0.1:5432/subscree"
    # redis
    celery_broker: RedisDsn = "redis://127.0.0.1:6379/0"
    # frequency that we check for due bills in seconds
    due_bills_checker_frequency: int = 3600

    class Config:
        env_file = ".env"


settings = Settings()
