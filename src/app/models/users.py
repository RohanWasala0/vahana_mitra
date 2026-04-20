from __future__ import annotations

from datetime import datetime
from typing import Sequence
from uuid import uuid4

from sqlalchemy import DateTime, Index, String, Text, event, func, select
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.engine import Connection
from sqlalchemy.orm import Mapped, Session, mapped_column
from flask_security.models import fsqla_v3 as fsqla

from app.extensions import db

fsqla.FsModels.set_db_info(db, user_table_name="users", role_table_name="roles")


class Role(db.Model, fsqla.FsRoleMixin):
    __tablename__ = "roles"
    pass


class User(db.Model, fsqla.FsUserMixin):
    __tablename__ = "users"

    phone: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, default="")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    alternate_id: Mapped[str] = mapped_column(
        String, default=lambda: uuid4().hex, index=True
    )

    # relationship
    # truck = relationship(
    #     "TRUCKS", backref="USERS", lazy=True, cascade="all, delete-orphan"
    # )
    # load = relationship(
    #     "LOADS", backref="USERS", lazy=True, cascade="all, delete-orphan"
    # )

    # Full-text search vector: TSVECTOR on Postgres, TEXT elsewhere (e.g., SQLite tests).
    search_vector: Mapped[str | None] = mapped_column(
        Text().with_variant(TSVECTOR(), "postgresql"),
        nullable=True,
    )

    __table_args__ = (
        # Postgres GIN index for fast full-text search.
        Index("ix_users_search_vector", "search_vector", postgresql_using="gin"),
    )

    @staticmethod
    def search(session: Session, query: str, limit: int = 20) -> Sequence["User"]:
        """
        Example search:
          - Postgres: tsvector @@ plainto_tsquery
          - Other DBs: fallback to ILIKE pattern search on name/email
        """
        bind = session.get_bind()
        dialect = getattr(bind, "dialect", None)

        if dialect is not None and dialect.name == "postgresql":
            tsq = func.plainto_tsquery("english", query)
            stmt = (
                select(User)
                .where(User.search_vector.op("@@")(tsq))
                .order_by(User.created_at.desc())
                .limit(limit)
            )
        else:
            pattern = f"%{query}%"
            stmt = (
                select(User)
                .where((User.alternate_id.ilike(pattern)))
                .order_by(User.created_at.desc())
                .limit(limit)
            )

        return list(session.scalars(stmt))


@event.listens_for(User, "before_insert")
def _user_before_insert(_mapper: object, connection: Connection, target: User) -> None:
    if connection.dialect.name == "postgresql":
        target.search_vector = func.to_tsvector(
            "english",
            func.concat_ws(" ", target.alternate_id, target.email),
        )


@event.listens_for(User, "before_update")
def _user_before_update(_mapper: object, connection: Connection, target: User) -> None:
    if connection.dialect.name == "postgresql":
        target.search_vector = func.to_tsvector(
            "english",
            func.concat_ws(" ", target.alternate_id, target.email),
        )
