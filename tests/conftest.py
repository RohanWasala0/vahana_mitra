from __future__ import annotations

import pytest
from flask import Flask

from app import create_app
from app.extensions import db


@pytest.fixture()
def app() -> Flask:
    flask_app = create_app("testing")

    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app: Flask):
    return app.test_client()
