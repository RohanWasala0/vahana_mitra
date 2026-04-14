from __future__ import annotations

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin


db: SQLAlchemy = SQLAlchemy()
migrate: Migrate = Migrate()
admin: Admin = Admin()


def init_extensions(app: Flask) -> None:
    """
    Initialize Flask extensions in a single, testable place.
    """
    db.init_app(app)
    migrate.init_app(app, db)
