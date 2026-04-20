from __future__ import annotations

import random
import secrets
from typing import Iterable

import click
from flask_security.core import UserMixin
from flask_security.utils import hash_password
from sqlalchemy import select
import sqlalchemy

from app.extensions import db
from app.security import user_datastore
from app.models.users import User, Role


def _random_email() -> str:
    return f"user_{secrets.token_hex(4)}@example.com"


def _random_name() -> str:
    return f"User {secrets.token_hex(2)}"


def _random_phone() -> str:
    return str(random.random())


def _ensure_admin(
    email: str = "admin@example.com", phone: str = "000"
) -> User | UserMixin:
    user_datastore.find_or_create_role(name="admin")
    existing = user_datastore.find_user(email=email)

    if existing:
        if not any(getattr(r, "name", None) == "admin" for r in existing.roles):
            user_datastore.add_role_to_user(existing, "admin")

        db.session.commit()
        return existing

    pw = "admin@1412"

    admin = user_datastore.create_user(
        email=email,
        phone=phone,
        name="Admin User",
        roles=["admin"],
        password=pw,
    )
    db.session.commit()
    return admin


def _create_users(n: int) -> Iterable[UserMixin]:
    for _ in range(n):
        u = user_datastore.create_user(
            email=_random_email(),
            phone=_random_phone(),
            name=_random_name(),
        )
        db.session.commit()
        yield u


@click.command("seed-db")
@click.option("--users", "users_count", default=25, show_default=True, type=int)
@click.option("--reset", is_flag=True, help="Delete existing rows before seeding.")
def seed_db(users_count: int, reset: bool) -> None:
    """
    Seed the database with dummy data for local testing (Flask-Admin, etc.).

    Creates/ensures:
      - admin@example.com (is_admin=True)
      - N normal users
    """
    if reset:
        # For real apps, you might want per-model deletes.
        db.session.execute(sqlalchemy.text("DELETE FROM roles_users"))

        # Then delete children/parents
        db.session.execute(sqlalchemy.delete(User))
        db.session.execute(sqlalchemy.delete(Role))

        db.session.commit()

    db.create_all()
    _ensure_admin()
    list(_create_users(users_count))

    db.session.commit()
    click.echo(f"Seeded: 1 admin + {users_count} users")
