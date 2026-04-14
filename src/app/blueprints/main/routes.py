from __future__ import annotations

from flask import Response, jsonify, render_template

from app.blueprints.main import bp


@bp.get("/")
def index() -> str:
    return render_template("index.html")


@bp.get("/health")
def health() -> Response:
    # No DB access by design.
    return jsonify({"status": "ok"})
