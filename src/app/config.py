from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
import secrets


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
    SECURITY_PASSWORD_SALT: str = os.environ.get(
        "SECURITY_PASSWORD_SALT", str(secrets.SystemRandom().getrandbits(128))
    )
    DEBUG: bool = _env_bool("FLASK_DEBUG", False)
    TESTING: bool = False

    # Security
    SECURITY_ANONYMOUS_USER_DISABLED = True
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Security URLs, overridden because they don't put a / at the end
    SECURITY_BLUEPRINT_NAME = "security"
    SECURITY_URL_PREFIX = ""
    SECURITY_LOGIN_URL = "/login"
    SECURITY_LOGOUT_URL = "/logout/"
    SECURITY_REGISTER_URL = "/register/"
    SECURITY_POST_LOGIN_VIEW = "/admin/"
    SECURITY_POST_LOGOUT_VIEW = "/admin/"
    SECURITY_POST_REGISTER_VIEW = "/admin/"

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
    DEBUG: bool = True

    BASE_DIR = Path(__file__).resolve().parent
    DB_PATH = BASE_DIR / "instance" / "dev.db"
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    SQLALCHEMY_DATABASE_URI: str = f"sqlite+pysqlite:///{DB_PATH}"

    def __post_init__(self) -> None:  # pragma: no cover
        super().__post_init__()
        object.__setattr__(self, "SQLALCHEMY_ENGINE_OPTIONS", {"pool_pre_ping": True})
