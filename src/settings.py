from pydantic import BaseSettings, PostgresDsn, RedisDsn


class Settings(BaseSettings):
    # DB
    database_url: PostgresDsn = "postgresql://subscree:subscree@127.0.0.1:5432/subscree"
    # redis
    celery_broker: RedisDsn = "redis://127.0.0.1:6379/0"
    # invoice reminder days
    invoice_reminder_days = 2
    # frequency that we check for due bills in seconds
    due_bills_checker_frequency: int = 3600

    SECRET_KEY = "123"  # TODO - store in env

    class Config:
        env_file = ".env"


settings = Settings()
