from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import (
    SelectField,
    IntegerField,
    StringField,
    FileField,
    DateField,
    SubmitField,
    TelField,
)
from wtforms.validators import DataRequired, Length, Regexp

VEHICLE_TYPE_CHOICES = [
    ("open", "Open"),
    ("close", "Closed"),
    ("container", "Container"),
    ("tanker", "Tanker"),
]

RTO_NUMBER_REGEX = r"^[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}"
AADHAAR_REGEX = r"^[2-9]{1}[0-9]{3}[0-9]{4}[0-9]{4}"
PAN_REGEX = r"^[A-Z]{5}[0-9]{4}[A-Z]{1}"


class TruckRegistrationForm(FlaskForm):
    user_id: SelectField = SelectField(
        "Select Existing User",
        validators=[DataRequired(message="Please select a user for this truck.")],
    )
    truck_current_location = StringField(
        "Current location from ", validators=[DataRequired()]
    )  # Auto GPS detection in future
    vehicle_registration_number: StringField = StringField(
        "Registration number", validators=[DataRequired(), Length(min=9, max=10)]
    )
    vehicle_model_name = SelectField(
        "Truck Model",
        choices=[
            ("", "Select Truck Model"),
            # Tata Motors
            ("Tata Ace", "Tata Ace"),
            ("Tata Intra", "Tata Intra"),
            ("Tata Yodha Pickup", "Tata Yodha Pickup"),
            ("Tata 407 Gold SFC", "Tata 407 Gold SFC"),
            ("Tata LPT", "Tata LPT"),
            ("Tata Ultra", "Tata Ultra"),
            ("Tata Signa", "Tata Signa"),
            ("Tata Prima", "Tata Prima"),
            # Ashok Leyland
            ("Ashok Leyland Dost", "Ashok Leyland Dost"),
            ("Ashok Leyland Bada Dost", "Ashok Leyland Bada Dost"),
            ("Ashok Leyland Partner", "Ashok Leyland Partner"),
            ("Ashok Leyland Boss", "Ashok Leyland Boss"),
            ("Ashok Leyland ecomet", "Ashok Leyland ecomet"),
            ("Ashok Leyland AVTR", "Ashok Leyland AVTR"),
            # BharatBenz
            ("BharatBenz LDT", "BharatBenz LDT"),
            ("BharatBenz MDT", "BharatBenz MDT"),
            ("BharatBenz HDT R", "BharatBenz HDT R"),
            ("BharatBenz HDT RT", "BharatBenz HDT RT"),
            ("BharatBenz HDT C", "BharatBenz HDT C"),
            ("BharatBenz HDT T", "BharatBenz HDT T"),
            # Eicher
            ("Eicher Pro 2000", "Eicher Pro 2000 Series"),
            ("Eicher Pro 3000", "Eicher Pro 3000 Series"),
            ("Eicher Pro 5000", "Eicher Pro 5000 Series"),
            ("Eicher Pro 6000", "Eicher Pro 6000 Series"),
            # Mahindra
            ("Mahindra Jeeto", "Mahindra Jeeto"),
            ("Mahindra Supro", "Mahindra Supro"),
            ("Mahindra Bolero Pikup", "Mahindra Bolero Pikup"),
            ("Mahindra Loadking", "Mahindra Loadking"),
            ("Mahindra Furio", "Mahindra Furio"),
            ("Mahindra Blazo X", "Mahindra Blazo X"),
            # SML Isuzu / SML Mahindra
            ("SML Sartaj", "SML Sartaj"),
            ("SML Samrat", "SML Samrat"),
            ("SML Supreme", "SML Supreme"),
            ("SML Prestige", "SML Prestige"),
            # Force Motors
            ("Force Traveller Delivery Van", "Force Traveller Delivery Van"),
            ("Force Traveller Wide Body", "Force Traveller Wide Body"),
            # Volvo
            ("Volvo FM", "Volvo FM"),
            ("Volvo FMX", "Volvo FMX"),
            # fallback
            ("Other", "Other"),
        ],
        validators=[DataRequired(message="Please select a truck model.")],
    )
    other_vehicle_model_name = StringField("Other Truck Model")
    vehicle_type = SelectField(
        "Lorry type Needed",
        choices=VEHICLE_TYPE_CHOICES,
        validators=[DataRequired()],
    )
    vehicle_capacity = IntegerField(
        "Max load capacity in tons", validators=[DataRequired()]
    )
    vehicle_insurance = FileField("Vehicle Insurance")
    vehicle_permit = StringField("Vehicle permits")

    truck_owner_name = StringField("Owners name", validators=[Length(min=10)])
    truck_owner_phone = TelField("Phone Number", validators=[Length(min=10, max=20)])
    truck_owner_aadhaar = StringField(
        "Owners Aadhaar number",
        validators=[Regexp(AADHAAR_REGEX, message="Write a valid aadhaar number")],
    )
    truck_owner_pan = StringField(
        "Owners PAN card number",
        validators=[Regexp(PAN_REGEX, message="Enter a valid PAN number")],
    )

    truck_driver_name = StringField("Driver Name")
    truck_driver_phone = StringField("Driver Phone number")
    truck_driver_aadhaar = StringField("Driver Aadhaar")
    truck_driver_license = FileField("Driver Driving License")

    available_date = DateField("Date Available")
    destionation_preference = StringField("Prefered destination location")
    request_load = SubmitField("Available for load requests")
    submit = SubmitField("Register Truck")
