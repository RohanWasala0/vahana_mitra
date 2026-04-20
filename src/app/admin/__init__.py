from __future__ import annotations

from flask import Flask

from app.extensions import admin, db
from app.models.users import User
from app.admin.views import SecureIndexView, UserAdminView


def init_admin(app: Flask):
    admin.init_app(app, index_view=SecureIndexView())
    admin.add_view(UserAdminView(User, db.session, name="Users", endpoint="user"))
