from __future__ import annotations

from flask import abort, flash, redirect, request, url_for
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose
from flask_login import current_user
from typing import Any

from app.forms.trucks import TruckRegistrationForm
from app.models import User, Truck
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


class AdminView(AdminIndexView):
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

    pass


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


class TruckAdminView(ModelView):
    create_template = "testing.html"
    column_list = (
        "truck_id",
        "user_id",
        "vehicle_registration_number",
        "vehicle_model_name",
        "vehicle_type",
        "vehicle_capacity",
        "current_location",
        "is_verified",
        "is_available",
        "truck_owner_name",
        "truck_owner_phone",
        "truck_owner_aadhaar",
        "truck_owner_pan",
        "truck_driver_name",
        "truck_driver_phone",
        "truck_driver_aadhaar",
        "truck_driver_license",
    )

    # ---- Inline editable columns ----
    column_editable_list = ("is_verified", "is_available", "current_location")

    def _get_user_dropdown(self):
        return User.query.order_by(User.name.asc()).all()

    def _set_user_choice(self, form):
        users = self._get_user_dropdown()

        form.user_id.choices = [(0, "Select truck owner")] + [
            (
                user.id,
                f"{user.name} - {getattr(user, 'phone', 'N/A') or getattr(user, 'email', 'N/A')}",
            )
            for user in users
        ]

        return users

    @expose("/new/", methods=["GET", "POST"])
    def create_view(self):
        form = TruckRegistrationForm()
        _ = self._set_user_choice(form)
        user_create_url = url_for("users.create_view", url=request.url)
        return_url = request.args.get("url") or self.get_url(".index_view")

        if request.method == "POST":
            if request.form.get("make_new_user") == "1":
                flash(
                    "Create the user first, then come back and register the truck.",
                    "info",
                )
                return redirect(user_create_url)
            if form.validate_on_submit():
                selected_user = db.session.get(User, form.user_id.data)

                if not selected_user:
                    form.user_id.errors = [
                        *form.user_id.errors,
                        "Select user is invalid",
                    ]

                else:
                    vehicle_model_name = (
                        form.vehicle_model_name.data
                        if form.vehicle_model_name.data != "Other"
                        else form.other_vehicle_model_name.data
                    )
                    print(form.vehicle_capacity.data)
                    truck = Truck(
                        user_id=selected_user.id,
                        # Vehical info
                        current_location=form.truck_current_location.data or "",
                        vehicle_registration_number=form.vehicle_registration_number.data,
                        vehicle_type=form.vehicle_type.data,
                        vehicle_capacity=form.vehicle_capacity.data,
                        vehicle_model_name=vehicle_model_name,
                        # Owner info
                        truck_owner_name=form.truck_owner_name.data,
                        truck_owner_phone=form.truck_owner_phone.data,
                        truck_owner_aadhaar=form.truck_owner_aadhaar.data,
                        truck_owner_pan=form.truck_owner_pan.data,
                        # Driver info
                        truck_driver_name=form.truck_driver_name.data,
                        truck_driver_phone=form.truck_driver_phone.data,
                        truck_driver_aadhaar=form.truck_driver_aadhaar.data,
                        # truck_driver_license
                    )

                    db.session.add(truck)
                    db.session.commit()
                    return redirect(return_url)

        return self.render(
            self.create_template,
            form=form,
            user_create_url=user_create_url,
            return_url=return_url,
        )
