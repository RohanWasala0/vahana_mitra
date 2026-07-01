from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    SelectField,
    IntegerField,
    StringField,
    TextAreaField,
    DateField,
    SubmitField,
)
from wtforms.validators import DataRequired, Length, Optional

VEHICLE_TYPE_CHOICES = [
    ("open", "Open"),
    ("close", "Closed"),
    ("container", "Container"),
    ("tanker", "Tanker"),
]
LOAD_TYPE_CHOICES = [
    ("construction", "Construction Materials"),
    ("agriculture", "Agricultural Produce"),
    ("chemicals", "Industrial Chemicals"),
    ("furniture", "Furniture"),
    ("electronics", "Electronics"),
    ("machinery", "Heavy Machinery"),
    ("packaged", "Packaged Goods"),
    ("liquid", "Liquid Cargo"),
    ("perishables", "Perishable Goods"),
    ("scrap", "Metal Scrap"),
]


class LoadScheduleForm(FlaskForm):
    user_id: SelectField = SelectField(
        "Select Existing User",
        validators=[DataRequired(message="Please select a user for this truck.")],
    )
    scheduling_compan: BooleanField = BooleanField()

    pickup_location = StringField("Pickup Location", validators=[DataRequired()])
    pickup_datetime = DateField("Pickup date", validators=[DataRequired()])
    pickup_contact_name = StringField(
        "Full Name", validators=[Length(min=2, max=80), DataRequired()]
    )
    pickup_contact_phone = StringField(
        "Phone Number", validators=[Length(min=10), DataRequired()]
    )
    pickup_map_coordinates = StringField("Map Location")
    pickup_instruction = StringField()

    drop_location = StringField("Drop Location", validators=[DataRequired()])
    drop_datetime = DateField("Drop date")
    drop_contact_name = StringField("Full Name", validators=[Length(min=2, max=80)])
    drop_contact_phone = StringField(
        "Phone Number", validators=[DataRequired(), Length(min=10)]
    )

    load_weight = IntegerField("Estimated Weight in tons", validators=[DataRequired()])
    vehicle_type = SelectField(
        "Lorry type Needed",
        choices=VEHICLE_TYPE_CHOICES,
        validators=[DataRequired()],
    )
    load_details = TextAreaField("Material Details", validators=[DataRequired()])
    load_type = SelectField(
        "Type of Materials",
        choices=LOAD_TYPE_CHOICES,
        validators=[DataRequired()],
    )

    request_truck = SubmitField("Request Lorry")
    admin_notes = TextAreaField(
        "Admin Notes",
        validators=[Optional(), Length(max=1000)],
    )
    submit = SubmitField("Register the Material")
