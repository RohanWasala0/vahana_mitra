from __future__ import annotations

from flask import abort, redirect, request, url_for
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from wtforms import PasswordField, SelectField
from typing import Any


class SecureModelView:
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


class SecureIndexView(SecureModelView, AdminIndexView):
    pass


class UserAdminView(ModelView):
    """Admin view for the User model with customizations.

    Columns:
    --------:
        id: User ID
        fullname: Full name of the user
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
    form_extra_fields = {
        "password": PasswordField("Password"),
    }

    # column to show number of trucks and loads for each user
    column_list = (
        "id",
        "fullname",
        "email",
        "phone",
        "is_admin",
        "truck_count",
        "load_count",
        "password",
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
