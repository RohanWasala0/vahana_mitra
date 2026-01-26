from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Mapping

from flask import Flask
from sqlalchemy.pool import StaticPool


def _env(name: str) -> str | None:
    value = os.getenv(name)
    if value is not None and value.strip() == "":
        return None
    return value


@dataclass(frozen=True)
class Config:
    # Flask
    DEBUG: bool = False
    TESTING: bool = False

    # Populated from env at runtime:
    SECRET_KEY: str | None = None

    # SQLAlchemy / Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI: str | None = None
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_ENGINE_OPTIONS: Mapping[str, Any] = None  # type: ignore[assignment]

    # Logging
    LOG_LEVEL: str = "INFO"

    @classmethod
    def load_from_env(cls, app: Flask) -> None:
        """
        Load required runtime values from environment variables.
        This avoids evaluating env vars at import-time (better for tests and tooling).
        """
        app.config["SECRET_KEY"] = app.config.get("SECRET_KEY") or _env("SECRET_KEY")
        database_url = app.config.get("SQLALCHEMY_DATABASE_URI") or _env("DATABASE_URL")
        app.config["SQLALCHEMY_DATABASE_URI"] = database_url
        app.config["DATABASE_URL"] = database_url  # convenience mirror

        app.config["LOG_LEVEL"] = app.config.get("LOG_LEVEL") or (
            _env("LOG_LEVEL") or "INFO"
        )

        # Sensible Postgres defaults (safe even if overridden)
        app.config.setdefault(
            "SQLALCHEMY_ENGINE_OPTIONS",
            {
                "pool_pre_ping": True,
                "pool_recycle": 300,
            },
        )

    @classmethod
    def validate(cls, app: Flask) -> None:
        """
        Enforce required configuration from environment.
        For TESTING, the TestingConfig supplies safe defaults, so we don't require env vars.
        """
        if app.config.get("TESTING", False):
            return

        required = ["SECRET_KEY", "SQLALCHEMY_DATABASE_URI"]
        missing = [k for k in required if not app.config.get(k)]
        if missing:
            raise RuntimeError(
                f"Missing required environment/config values: {', '.join(missing)}. "
                "Set them in your environment or in a local .env file."
            )


@dataclass(frozen=True)
class DevelopmentConfig(Config):
    DEBUG: bool = True


@dataclass(frozen=True)
class ProductionConfig(Config):
    DEBUG: bool = False


@dataclass(frozen=True)
class TestingConfig(Config):
    TESTING: bool = True
    SECRET_KEY: str = "testing-secret-key"
    SQLALCHEMY_DATABASE_URI: str = "sqlite+pysqlite:///:memory:"
    SQLALCHEMY_ENGINE_OPTIONS: Mapping[str, Any] = None  # type: ignore[assignment]

    @classmethod
    def load_from_env(cls, app: Flask) -> None:
        # Ignore external DB; keep tests hermetic and fast.
        app.config["SECRET_KEY"] = cls.SECRET_KEY
        app.config["SQLALCHEMY_DATABASE_URI"] = cls.SQLALCHEMY_DATABASE_URI
        app.config["DATABASE_URL"] = cls.SQLALCHEMY_DATABASE_URI
        app.config["LOG_LEVEL"] = "WARNING"

        # Ensure a single in-memory DB across connections.
        app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
            "connect_args": {"check_same_thread": False},
            "poolclass": StaticPool,
        }
