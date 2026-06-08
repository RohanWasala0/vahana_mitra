from flask_wtf import FlaskForm
from wtforms import (
    SelectField,
    IntegerField,
    StringField,
    FileField,
    DateField,
    SubmitField,
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
    user_id = SelectField(
        "Select Existing User",
        validators=[DataRequired(message="Please select a user for this truck.")],
    )
    truck_current_location = StringField(
        "Current location from ", validators=[DataRequired()]
    )  # Auto GPS detection in future
    vehicle_registration_number = StringField(
        "Registration number", validators=[DataRequired(), Length(min=9, max=10)]
    )
    vehicle_model_name = StringField("Trucks Model", validators=[DataRequired()])
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
    truck_owner_phone = StringField("Phone Number", validators=[Length(min=10, max=20)])
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
