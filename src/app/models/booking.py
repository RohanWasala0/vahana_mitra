from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db


class Booking(db.Model):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
