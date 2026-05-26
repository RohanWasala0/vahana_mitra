from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, String, Float, Boolean

from app.extensions import db


class Truck(db.Model):
    __tablename__ = "trucks"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    # Vehicle information
    vehicle_registration_number: Mapped[str] = mapped_column(String, nullable=False)
    vehicle_model_name: Mapped[str] = mapped_column(String, nullable=False)
    vehicle_type: Mapped[str] = mapped_column(String, nullable=False)
    vehicle_capacity: Mapped[float] = mapped_column(Float, nullable=False)
    vehicle_insurance: Mapped[str] = mapped_column(String, nullable=True)
    current_location: Mapped[str] = mapped_column(String, nullable=False)

    # Owner details
    truck_owner_name: Mapped[str] = mapped_column(String, nullable=False)
    truck_owner_phone: Mapped[str] = mapped_column(String, nullable=False)
    truck_owner_aadhaar: Mapped[str] = mapped_column(String, nullable=False)
    truck_owner_pan: Mapped[str] = mapped_column(String, nullable=True)

    # Driver details
    truck_driver_name: Mapped[str] = mapped_column(String, nullable=True)
    truck_driver_phone: Mapped[str] = mapped_column(String, nullable=True)
    truck_driver_aadhaar: Mapped[str] = mapped_column(String, nullable=True)
    truck_driver_license: Mapped[str] = mapped_column(String, nullable=True)

    # Status and documents
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    tds: Mapped[str] = mapped_column(String, nullable=True)
