from __future__ import annotations

import os
from typing import Type

from dotenv import load_dotenv
from flask import Flask

# from app.blueprints.main import bp as main_bp
# from app.config import Config, DevelopmentConfig, ProductionConfig, TestingConfig
# from app.extensions import init_extensions
# from app.logging import configure_logging


# _CONFIG_MAP: dict[str, Type[Config]] = {
#     "development": DevelopmentConfig,
#     "production": ProductionConfig,
#     "testing": TestingConfig,
# }
#
#
# def create_app(config_object: Type[Config] | None = None) -> Flask:
#     """
#     Flask application factory.
#
#     - Loads .env in local development (python-dotenv).
#     - Applies config object (or selects from APP_ENV).
#     - Validates required environment variables (SECRET_KEY, DATABASE_URL) for non-testing.
#     - Configures structured logging (console + rotating file).
#     - Initializes extensions (SQLAlchemy, Migrate).
#     - Registers blueprints.
#     """
#     app_env = (os.getenv("APP_ENV") or "development").lower()
#
#     # Load .env only for local development ergonomics.
#     # Flask CLI will also load .env automatically when python-dotenv is installed,
#     # but this keeps gunicorn/other entrypoints consistent.
#     if app_env == "development":
#         load_dotenv(override=False)
#
#     cfg_cls = config_object or _CONFIG_MAP.get(app_env, DevelopmentConfig)
#
#     app = Flask(
#         __name__,
#         template_folder="templates",
#         static_folder="static",
#     )
#
#     # Load class defaults.
#     app.config.from_object(cfg_cls)
#
#     # Load required secrets/URLs from environment at runtime (not import time).
#     cfg_cls.load_from_env(app)
#     cfg_cls.validate(app)
#
#     # Logging should come early so startup issues are visible.
#     configure_logging(app)
#
#     # Extensions and blueprints
#     init_extensions(app)
#     app.register_blueprint(main_bp)
#
#     return app
