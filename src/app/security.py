from __future__ import annotations

from flask import Flask, url_for
from flask_security.datastore import SQLAlchemyUserDatastore
import helpers as admin_helpers

from app.extensions import db, security, admin
from app.models import Role, User

user_datastore: SQLAlchemyUserDatastore = SQLAlchemyUserDatastore(db, User, Role)


def init_security(app: Flask) -> None:
    # Register Flask-Security blueprint (/login, /register, /logout, etc.)
    security.init_app(app, datastore=user_datastore)


@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.theme.base_template,
        admin_view=admin.index_view,
        theme=admin.theme,
        h=admin_helpers,
        get_url=url_for,
    )
