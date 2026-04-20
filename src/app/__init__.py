from __future__ import annotations

from typing import Any, Mapping, Type

from flask import Flask

from app.cli import seed_db
from app.admin import init_admin
from app.config import (
    Config,
    DevelopmentConfig,
    ProductionConfig,
    TestingConfig,
    resolve_environment,
)
from app.extensions import init_extensions
from app.logging_config import configure_logging
from app.security import init_security, security_context_processor


def create_app(
    config_name: str | None = None,
    config_overrides: Mapping[str, Any] | None = None,
) -> Flask:
    """
    Flask application factory.

    Args:
        config_name: Optional environment name: "development" | "production" | "testing".
        config_overrides: Optional dict of config overrides (useful for tests).

    Returns:
        Configured Flask app instance.
    """
    env = resolve_environment(config_name)

    config_cls: Type[Config]
    if env == "production":
        config_cls = ProductionConfig
    elif env == "testing":
        config_cls = TestingConfig
    else:
        config_cls = DevelopmentConfig

    app = Flask(
        __name__,
        instance_relative_config=False,
        template_folder="./templates/",
    )
    app.config.from_object(config_cls)

    if config_overrides:
        app.config.update(config_overrides)

    # Logging first so startup issues are captured.
    configure_logging(app)

    # Security assertions for production
    if env == "production":
        _validate_production_config(app.config)

    # Initialize extensions (db, migrate)
    init_extensions(app)
    init_security(app)
    init_admin(app)
    app.cli.add_command(seed_db)

    from app import models

    # Register blueprints
    from app.blueprints.main import bp as main_bp

    app.register_blueprint(main_bp)
    return app


def _validate_production_config(cfg: Mapping[str, Any]) -> None:
    secret_key = str(cfg.get("SECRET_KEY") or "")
    if not secret_key or secret_key.lower().strip() in {"change-me", "changeme"}:
        raise RuntimeError(
            "Production requires a strong SECRET_KEY (do not use 'change-me')."
        )

    db_url = str(cfg.get("SQLALCHEMY_DATABASE_URI") or "")
    if not db_url:
        raise RuntimeError(
            "Production requires DATABASE_URL / SQLALCHEMY_DATABASE_URI."
        )
