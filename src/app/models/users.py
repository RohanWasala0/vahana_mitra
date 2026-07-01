from __future__ import annotations

from datetime import datetime
from typing import Sequence
from uuid import uuid4

from flask_security.models import fsqla_v3 as fsqla
from sqlalchemy import DateTime, Index, String, Text, event, func, or_, select
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.engine import Connection
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship

from app.extensions import db


# This creates Flask-Security's roles_users association table using:
#   users.id
#   roles.id
fsqla.FsModels.set_db_info(
    db,
    user_table_name="users",
    role_table_name="roles",
)


class Role(db.Model, fsqla.FsRoleMixin):
    __tablename__ = "roles"

    # FsRoleMixin already supplies:
    # id, name, description, permissions, update_datetime
    pass


class User(db.Model, fsqla.FsUserMixin):
    __tablename__ = "users"

    # FsUserMixin already supplies:
    # id, email, password, active, fs_uniquifier, roles,
    # create_datetime, update_datetime, and security-related fields.

    # Keep nullable unless every Flask-Security registration flow supplies it.
    phone: Mapped[str | None] = mapped_column(
        String(20),
        unique=True,
        index=True,
        nullable=True,
    )

    name: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
        default="",
    )

    alternate_id: Mapped[str] = mapped_column(
        String(32),
        default=lambda: uuid4().hex,
        unique=True,
        index=True,
        nullable=False,
    )

    company_info: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    gst_no: Mapped[str | None] = mapped_column(
        String(15),
        unique=True,
        nullable=True,
    )

    gst_filepath: Mapped[str | None] = mapped_column(
        String(512),
        nullable=True,
    )

    # These are collection relationships despite the singular attribute names.
    # Rename to `trucks` and `loads` when practical.
    truck = relationship(
        "Truck",
        backref="users",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    load = relationship(
        "Load",
        backref="users",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    # PostgreSQL: TSVECTOR
    # SQLite/tests: TEXT
    search_vector: Mapped[str | None] = mapped_column(
        Text().with_variant(TSVECTOR(), "postgresql"),
        nullable=True,
    )

    __table_args__ = (
        Index(
            "ix_users_search_vector",
            "search_vector",
            postgresql_using="gin",
        ).ddl_if(dialect="postgresql"),
    )

    @classmethod
    def search(
        cls,
        session: Session,
        query: str,
        limit: int = 20,
    ) -> Sequence[User]:
        """
        Search users.

        PostgreSQL:
            Uses the GIN-indexed TSVECTOR, with exact matching for identifiers.

        Other databases:
            Uses case-insensitive pattern matching.
        """
        query = query.strip()

        if not query or limit <= 0:
            return []

        # Avoid accidentally returning an unbounded result set.
        limit = min(limit, 100)

        bind = session.get_bind()
        dialect_name = bind.dialect.name

        if dialect_name == "postgresql":
            ts_query = func.plainto_tsquery("simple", query)

            statement = (
                select(cls)
                .where(
                    or_(
                        cls.search_vector.op("@@")(ts_query),
                        cls.alternate_id == query,
                        func.lower(cls.email) == query.lower(),
                        cls.phone == query,
                        func.upper(cls.gst_no) == query.upper(),
                    )
                )
                .limit(limit)
            )
        else:
            pattern = f"%{query}%"

            statement = (
                select(cls)
                .where(
                    or_(
                        cls.alternate_id.ilike(pattern),
                        cls.name.ilike(pattern),
                        cls.phone.ilike(pattern),
                        cls.company_info.ilike(pattern),
                        cls.gst_no.ilike(pattern),
                    )
                )
                .limit(limit)
            )

        return session.scalars(statement).all()


@event.listens_for(User, "before_insert")
@event.listens_for(User, "before_update")
def _update_user_search_vector(
    _mapper: object,
    connection: Connection,
    target: User,
) -> None:
    values = (
        target.alternate_id,
        target.email,
        target.name,
        target.phone,
        target.company_info,
        target.gst_no,
    )

    if connection.dialect.name == "postgresql":
        # SQLAlchemy permits SQL expressions to be assigned to mapped
        # attributes during INSERT/UPDATE flushes.
        target.search_vector = func.to_tsvector(
            "simple",
            func.concat_ws(" ", *values),
        )  # type: ignore[assignment]
    else:
        # Useful for SQLite tests and inspecting the model.
        target.search_vector = " ".join(str(value) for value in values if value)
