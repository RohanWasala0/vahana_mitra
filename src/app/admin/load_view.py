from __future__ import annotations

from flask_admin import expose
from flask import url_for, request, flash, redirect

from app.admin.views import SecureModelView
from app.forms.loads import LoadScheduleForm
from app.models import User, Load
from app.extensions import db


class LoadModelView(SecureModelView):
    create_template = "/admin/load_schedule.html"

    def _get_user_dropdown(self):
        return User.query.order_by(User.name.asc()).all()

    def _set_user_choice(self, form):
        users = self._get_user_dropdown()

        form.user_id.choices = [(0, "Select User to schedule Load under")] + [
            (
                user.id,
                f"{user.name} - {getattr(user, 'phone', 'N/A') or getattr(user, 'email', 'N/A')}",
            )
            for user in users
        ]

        return users

    @expose("/new/", methods=["GET", "POST"])
    def create_view(self):

        form = LoadScheduleForm()
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
                    new_load = Load(
                        user_id=selected_user.id,
                        pickup_location=(
                            loc.strip()
                            if (loc := form.pickup_location.data) is not None
                            else ""
                        ),
                        pickup_datetime=form.pickup_datetime.data,
                        pickup_contact_name=form.pickup_contact_name.data or "",
                        pickup_contact_phone=form.pickup_contact_phone.data or "",
                        drop_location=form.drop_location.data or "",
                        drop_datetime=form.drop_datetime.data,
                        drop_contact_name=form.drop_contact_name.data or "",
                        drop_contact_phone=form.drop_contact_phone.data or "",
                        load_weight=form.load_weight.data or 0.0,
                        # vehicle_type=form.vehicle_type.data,
                        load_current_location="",
                        load_type=form.load_type.data.strip(),
                        load_details=form.load_details.data.strip()
                        if form.load_details.data
                        else None,
                        is_active=True,
                        in_progress=False,
                        # admin_notes=form.admin_notes.data.strip()
                        # if form.admin_notes.data
                        # else None,
                    )

                    db.session.add(new_load)
                    db.session.commit()
                    return redirect(return_url)

        return self.render(
            template=self.create_template, return_url=return_url, form=form
        )
