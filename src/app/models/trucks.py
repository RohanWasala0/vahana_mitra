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
    vehicle_insurance: Mapped[str | None] = mapped_column(String, nullable=True)
    current_location: Mapped[str | None] = mapped_column(String, nullable=True)

    # Owner details
    truck_owner_name: Mapped[str] = mapped_column(String, nullable=False)
    truck_owner_phone: Mapped[str] = mapped_column(String, nullable=False)
    truck_owner_aadhaar: Mapped[str] = mapped_column(String, nullable=False)
    truck_owner_pan: Mapped[str | None] = mapped_column(String, nullable=True)

    # Driver details
    truck_driver_name: Mapped[str | None] = mapped_column(String, nullable=True)
    truck_driver_phone: Mapped[str | None] = mapped_column(String, nullable=True)
    truck_driver_aadhaar: Mapped[str | None] = mapped_column(String, nullable=True)
    truck_driver_license: Mapped[str | None] = mapped_column(String, nullable=True)

    # Status and documents
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_available: Mapped[bool | None] = mapped_column(Boolean, default=True)
    # tds: Mapped[str] = mapped_column(String, nullable=True)

    def __init__(
        self,
        *,
        user_id: int,
        vehicle_registration_number: str,
        vehicle_model_name: str,
        vehicle_type: str,
        vehicle_capacity: float,
        current_location: str | None,
        truck_owner_name: str,
        truck_owner_phone: str,
        truck_owner_aadhaar: str,
        truck_owner_pan: str | None = None,
        vehicle_insurance: str | None = None,
        truck_driver_name: str | None = None,
        truck_driver_phone: str | None = None,
        truck_driver_aadhaar: str | None = None,
        truck_driver_license: str | None = None,
        is_verified: bool = False,
        is_available: bool = True,
    ) -> None:
        self.user_id = user_id

        self.vehicle_registration_number = vehicle_registration_number
        self.vehicle_model_name = vehicle_model_name
        self.vehicle_type = vehicle_type
        self.vehicle_capacity = vehicle_capacity
        self.vehicle_insurance = vehicle_insurance
        self.current_location = current_location

        self.truck_owner_name = truck_owner_name
        self.truck_owner_phone = truck_owner_phone
        self.truck_owner_aadhaar = truck_owner_aadhaar
        self.truck_owner_pan = truck_owner_pan

        self.truck_driver_name = truck_driver_name
        self.truck_driver_phone = truck_driver_phone
        self.truck_driver_aadhaar = truck_driver_aadhaar
        self.truck_driver_license = truck_driver_license

        self.is_verified = is_verified
        self.is_available = is_available
