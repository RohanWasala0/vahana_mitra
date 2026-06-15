from __future__ import annotations

from datetime import datetime, time
from typing import Any
from flask import abort, redirect, request, url_for
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, BaseView, expose
from flask_login import current_user
from sqlalchemy import func, select

from app.models import User, Truck, Load
from app.extensions import db


class SecureModelView(ModelView):
    """
    Base Admin view: deny by default; allow only authenticated users with admin role.
    """

    def is_accessible(self) -> bool:
        # current_user is a LocalProxy; treat as authenticated principal
        if not getattr(current_user, "is_authenticated", False):
            return False

        # Flask-Security FsUserMixin provides has_role()
        return bool(
            getattr(current_user, "has_role", None) and current_user.has_role("admin")
        )

    def inaccessible_callback(self, name: str, **kwargs: Any) -> Any:
        # Not logged in -> go to Flask-Security login
        if not getattr(current_user, "is_authenticated", False):
            return redirect(url_for("security.login", next=request.url))
        # Logged in but not authorized
        return abort(403)


class AdminDashboardView(AdminIndexView):
    def is_accessible(self) -> bool:
        # current_user is a LocalProxy; treat as authenticated principal
        if not getattr(current_user, "is_authenticated", False):
            return False

        # Flask-Security FsUserMixin provides has_role()
        return bool(
            getattr(current_user, "has_role", None) and current_user.has_role("admin")
        )

    def inaccessible_callback(self, name: str, **kwargs: Any) -> Any:
        # Not logged in -> go to Flask-Security login
        if not getattr(current_user, "is_authenticated", False):
            return redirect(url_for("security.login", next=request.url))
        # Logged in but not authorized
        return abort(403)

    @expose("/")
    def index(self):
        today_start = datetime.combine(datetime.utcnow().date(), time.min)
        active_load_statuses = [
            "PENDING",
            "ASSIGNED",
            "PICKED_UP",
            "IN_TRANSIT",
        ]

        def count_scalar(statement: Any) -> int:
            return int(db.session.scalar(statement) or 0)

        total_users = count_scalar(select(func.count(User.id)))

        # active_users = count_scalar(
        #     select(func.count(User.id)).where(User.is_active.is_(True))
        # )

        new_users_today = count_scalar(
            select(func.count(User.id)).where(User.created_at >= today_start)
        )

        total_trucks = count_scalar(select(func.count(Truck.id)))

        available_trucks = count_scalar(
            select(func.count(Truck.id)).where(Truck.is_available.is_(True))
        )

        busy_trucks = max(total_trucks - available_trucks, 0)

        total_loads = count_scalar(select(func.count(Load.id)))

        # active_loads = count_scalar(
        #     select(func.count(Load.id)).where(Load.status.in_(active_load_statuses))
        # )
        #
        # pending_loads = count_scalar(
        #     select(func.count(Load.id)).where(Load.status == "PENDING")
        # )
        #
        # assigned_loads = count_scalar(
        #     select(func.count(Load.id)).where(Load.status == "ASSIGNED")
        # )
        #
        # in_transit_loads = count_scalar(
        #     select(func.count(Load.id)).where(Load.status == "IN_TRANSIT")
        # )
        #
        # completed_loads = count_scalar(
        #     select(func.count(Load.id)).where(Load.status == "DELIVERED")
        # )
        #
        # cancelled_loads = count_scalar(
        #     select(func.count(Load.id)).where(Load.status == "CANCELLED")
        # )

        # loads_without_truck = count_scalar(
        #     select(func.count(Load.id)).where(
        #         Load.truck_id.is_(None),
        #         Load.status.in_(["PENDING", "ASSIGNED"]),
        #     )
        # )

        # load_status_rows = db.session.execute(
        #     select(
        #         Load.status,
        #         func.count(Load.id),
        #     )
        #     .group_by(Load.status)
        #     .order_by(Load.status)
        # ).all()

        # load_status_counts = {
        #     str(status): int(total) for status, total in load_status_rows
        # }

        # recent_loads = db.session.scalars(
        #     select(Load).order_by(Load.created_at.desc()).limit(10)
        # ).all()

        # recent_logs = db.session.scalars(
        #     select(ActivityLog).order_by(ActivityLog.created_at.desc()).limit(30)
        # ).all()

        available_truck_list = db.session.scalars(
            select(Truck)
            .where(Truck.is_available.is_(True))
            .order_by(Truck.id.desc())
            .limit(10)
        ).all()

        alerts: list[dict[str, str]] = []

        # if loads_without_truck > 0:
        #     alerts.append(
        #         {
        #             "level": "danger",
        #             "title": "Loads need truck assignment",
        #             "message": f"{loads_without_truck} active load(s) do not have a truck assigned.",
        #         }
        #     )

        if available_trucks == 0:
            alerts.append(
                {
                    "level": "warning",
                    "title": "No available trucks",
                    "message": "There are currently no available trucks for new load assignment.",
                }
            )

        # if pending_loads > 0 and available_trucks > 0:
        #     alerts.append(
        #         {
        #             "level": "info",
        #             "title": "Matching opportunity",
        #             "message": f"{pending_loads} pending load(s) can be matched with {available_trucks} available truck(s).",
        #         }
        #     )

        dashboard_data = {
            "total_users": total_users,
            "active_users": "",
            "new_users_today": new_users_today,
            "total_trucks": total_trucks,
            "available_trucks": available_trucks,
            "busy_trucks": busy_trucks,
            "total_loads": total_loads,
            "active_loads": "",
            "pending_loads": "",
            "assigned_loads": "",
            "in_transit_loads": "",
            "completed_loads": "",
            "cancelled_loads": "",
            "loads_without_truck": "",
            "load_status_counts": "",
            "recent_loads": "",
            "recent_logs": "",
            "available_truck_list": available_truck_list,
            "alerts": alerts,
        }
        return self.render("/admin/custom_dashboard.html", dashboard=dashboard_data)


class UserAdminView(SecureModelView):
    """Admin view for the User model with customizations.

    Columns:
    --------:
        id: User ID
        name: Full name of the user
        email: Email address of the user
        phone: Phone number of the user
        is_admin: Boolean indicating if the user is an admin
        truck_count: Number of trucks associated with the user
        load_count: Number of loads associated with the user
    """

    column_exclude_list = ("_password", "alternative_id")
    # column_editable_list = ('fullname', 'email', 'phone', 'is_admin')
    form_excluded_columns = (
        "alternative_id",
        "creation_time",
        "update_time",
        "truck_count",
        "load_count",
    )

    # column to show number of trucks and loads for each user
    column_list = (
        "id",
        "name",
        "email",
        "phone",
        "is_admin",
        "truck_count",
        "load_count",
    )

    # column_formatters = {
    #     "truck_count": lambda v, c, m, p: len(m.truck) if hasattr(m, "truck") else 0,
    #     "load_count": lambda v, c, m, p: len(m.load) if hasattr(m, "load") else 0,
    # }
    #
    # def get_query(self):
    #     return (
    #         super().get_query().options(joinedload(users.truck), joinedload(User.load))
    #     )
    #
    # def get_count_query(self):
    #     return super().get_count_query()
