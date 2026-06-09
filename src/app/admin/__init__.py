from __future__ import annotations

from flask import Flask

from app.admin.load_view import LoadModelView
from app.extensions import admin, db
from app.admin.views import (
    AdminDashboardView,
    SecureModelView,
    TruckAdminView,
    UserAdminView,
)
from app.models import User, Load, Truck


def init_admin(app: Flask) -> None:
    admin.init_app(app, index_view=AdminDashboardView())

    admin.add_view(UserAdminView(User, db.session, name="Users", endpoint="users"))
    admin.add_view(LoadModelView(Load, db.session, name="Loads"))
    admin.add_view(
        TruckAdminView(
            Truck,
            db.session,
            name="Trucks",
        )
    )
