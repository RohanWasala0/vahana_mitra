from __future__ import annotations

from flask import Flask
from flask_admin.contrib.sqla import ModelView
from wtforms import PasswordField, SelectField

from app.extensions import admin, db
from app.models.users import User


def init_admin(app: Flask):
    admin.init_app(app)
    admin.add_view(UserAdminView(User, db.session, endpoint="user"))


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
