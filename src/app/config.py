from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def resolve_environment(config_name: str | None) -> str:
    """
    Resolve environment name.

    Priority:
      1) explicit arg
      2) APP_ENV
      3) FLASK_ENV (legacy-compatible)
      4) default: development
    """
    if config_name:
        return config_name.strip().lower()

    return (
        (
            os.getenv("APP_ENV")
            or os.getenv("FLASK_ENV")  # compatibility
            or "development"
        )
        .strip()
        .lower()
    )


def _env_bool(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "y", "on"}


@dataclass(frozen=True)
class Config:
    # Core
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me")
    DEBUG: bool = _env_bool("FLASK_DEBUG", False)
    TESTING: bool = False

    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_DATABASE_URI: str = os.getenv("DATABASE_URL", "")
    SQLALCHEMY_ECHO: bool = _env_bool("SQLALCHEMY_ECHO", False)

    # Cookies / session security (overridden in ProductionConfig)
    SESSION_COOKIE_HTTPONLY: bool = True
    SESSION_COOKIE_SAMESITE: str = "Lax"
    SESSION_COOKIE_SECURE: bool = False

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()
    LOG_DIR: Path = Path(os.getenv("LOG_DIR", "logs"))
    LOG_FILE_NAME: str = "app.log"

    def __post_init__(self) -> None:  # pragma: no cover (dataclass hook)
        object.__setattr__(
            self,
            "SQLALCHEMY_ENGINE_OPTIONS",
            {
                "pool_pre_ping": True,
                "pool_recycle": 300,
            },
        )


class DevelopmentConfig(Config):
    DEBUG: bool = True

    def __post_init__(self) -> None:  # pragma: no cover
        super().__post_init__()
        # Load .env locally if python-dotenv is present; production should provide env vars externally.
        try:
            from dotenv import load_dotenv  # type: ignore

            load_dotenv(override=False)
        except Exception:
            pass


class ProductionConfig(Config):
    DEBUG: bool = False
    SESSION_COOKIE_SECURE: bool = True


class TestingConfig(Config):
    TESTING: bool = True
    DEBUG: bool = False

    # Prefer SQLite for fast, hermetic tests; allow opt-in Postgres via TEST_DATABASE_URL.
    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        "TEST_DATABASE_URL", "sqlite+pysqlite:///:memory:"
    )

    def __post_init__(self) -> None:  # pragma: no cover
        super().__post_init__()
        object.__setattr__(self, "SQLALCHEMY_ENGINE_OPTIONS", {"pool_pre_ping": True})
