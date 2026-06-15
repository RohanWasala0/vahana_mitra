from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, String, Float, Boolean, DateTime
from datetime import datetime

from app.extensions import db


class Load(db.Model):
    __tablename__ = "loads"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    # Pickup details
    pickup_location: Mapped[str] = mapped_column(String, nullable=False)
    pickup_datetime: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    pickup_contact_name: Mapped[str] = mapped_column(String, nullable=False)
    pickup_contact_phone: Mapped[str] = mapped_column(String, nullable=False)

    # Drop details
    drop_location: Mapped[str] = mapped_column(String, nullable=False)
    drop_datetime: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    drop_contact_name: Mapped[str] = mapped_column(String, nullable=False)
    drop_contact_phone: Mapped[str] = mapped_column(String, nullable=False)

    # Cargo details
    load_type: Mapped[str] = mapped_column(String, nullable=False)
    load_weight: Mapped[float] = mapped_column(Float, nullable=False)
    load_details: Mapped[str | None] = mapped_column(String, nullable=True)
    load_current_location: Mapped[str] = mapped_column(String, nullable=False)

    # Status and cost
    cost: Mapped[float | None] = mapped_column(Float, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    in_progress: Mapped[bool] = mapped_column(Boolean, default=False)

    @classmethod
    def find_available_loads(
        cls, capacity: int | None = None, current_location: str | None = None
    ):
        # query = cls.query.filter(cls.is_active == True, cls.in_progress == False)
        query = cls.query

        if capacity:
            query = query.filter(cls.load_weight <= capacity)
        if current_location:
            query = query.filter(cls.pickup_location.ilike(f"%{current_location}%"))

        return query.all()

    def __init__(
        self,
        *,
        user_id: int,
        pickup_location: str,
        pickup_datetime: datetime,
        pickup_contact_name: str,
        pickup_contact_phone: str,
        drop_location: str,
        drop_datetime: datetime,
        drop_contact_name: str,
        drop_contact_phone: str,
        load_type: str,
        load_weight: float,
        load_details: str | None = None,
        load_current_location: str,
        cost: int | None = None,
        is_active: bool,
        in_progress: bool,
    ) -> None:

        self.user_id = user_id
        self.pickup_location = pickup_location
        self.pickup_datetime = pickup_datetime
        self.pickup_contact_name = pickup_contact_name
        self.pickup_contact_phone = pickup_contact_phone
        self.drop_location = drop_location
        self.drop_datetime = drop_datetime
        self.drop_contact_name = drop_contact_name
        self.drop_contact_phone = drop_contact_phone
        self.load_type = load_type
        self.load_weight = load_weight
        self.load_details = load_details
        self.load_current_location = load_current_location
        self.cost = cost
        self.is_active = is_active
        self.in_progress = in_progress
