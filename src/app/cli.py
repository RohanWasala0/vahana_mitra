from __future__ import annotations

import random
import secrets
from typing import Iterable

import click
from sqlalchemy import select

from app.extensions import db
from app.models.users import User


def _random_email() -> str:
    return f"user_{secrets.token_hex(4)}@example.com"


def _random_name() -> str:
    return f"User {secrets.token_hex(2)}"


def _random_phone() -> str:
    return str(random.random())


def _ensure_admin(email: str = "admin@example.com", phone: str = "000") -> User:
    existing = db.session.scalar(select(User).where(User.email == email))
    if existing:
        existing.is_admin = True
        return existing

    admin = User(email=email, phone=phone, name="Admin User", is_admin=True)
    db.session.add(admin)
    return admin


def _create_users(n: int) -> Iterable[User]:
    for _ in range(n):
        u = User(
            email=_random_email(),
            phone=_random_phone(),
            name=_random_name(),
            is_admin=False,
        )
        db.session.add(u)
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
        db.session.execute(db.text("DELETE FROM users"))  # type: ignore[attr-defined]

    db.create_all()
    _ensure_admin()
    list(_create_users(users_count))

    db.session.commit()
    click.echo(f"Seeded: 1 admin + {users_count} users")
