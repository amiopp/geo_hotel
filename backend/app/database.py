from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DEFAULT_SQLITE_PATH = Path(__file__).resolve().parents[2] / "geohotel_insight.db"


class Settings(BaseSettings):
    database_url: str = f"sqlite:///{DEFAULT_SQLITE_PATH.as_posix()}"
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    login_identifier: str = "admin"
    login_password: str = "geohotel2026"
    login_display_name: str = "GeoHotel Analyste"
    login_token: str = "geohotel-local-session"

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, connect_args=connect_args, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
