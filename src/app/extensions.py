from __future__ import annotations

from flask import Flask
from flask_migrate import Migrate
from flask_security.core import Security
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager
from flask_babel import Babel

db: SQLAlchemy = SQLAlchemy()
migrate: Migrate = Migrate()
admin: Admin = Admin()
login_manager: LoginManager = LoginManager()
security: Security = Security()
babel: Babel = Babel()


def init_extensions(app: Flask) -> None:
    """
    Initialize Flask extensions in a single, testable place.
    """
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    babel.init_app(app)
