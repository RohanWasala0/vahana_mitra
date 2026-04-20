from __future__ import annotations

from flask import Response, jsonify, render_template
from flask_security.decorators import auth_required, roles_required

from app.blueprints.main import bp


@bp.get("/")
def index() -> str:
    return render_template("index.html")


@bp.get("/health")
def health() -> Response:
    # No DB access by design.
    return jsonify({"status": "ok"})


# @bp.get("/admin")
# @auth_required()
# @roles_required("admin")
# def admin_only():
#     pass
