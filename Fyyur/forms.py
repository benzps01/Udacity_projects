from datetime import datetime
from flask_wtf import Form
from wtforms import (
    StringField,
    SelectField,
    SelectMultipleField,
    DateTimeField,
    BooleanField,
)
from wtforms.validators import DataRequired, AnyOf, URL
from selectfields import State, Genre

# referenced from https://flask.palletsprojects.com/en/2.3.x/patterns/wtforms/ for the selectfields.py using enum


class ShowForm(Form):
    artist_id = StringField("artist_id", validators=[DataRequired()])
    venue_id = StringField("venue_id", validators=[DataRequired()])
    start_time = DateTimeField(
        "start_time", validators=[DataRequired()], default=datetime.today()
    )


class VenueForm(Form):
    name = StringField("name", validators=[DataRequired()])
    city = StringField("city", validators=[DataRequired()])
    state = SelectField(
        "state", validators=[DataRequired()], choices=State.state_choice()
    )
    address = StringField("address", validators=[DataRequired()])
    phone = StringField("phone", validators=[DataRequired()])
    image_link = StringField("image_link", validators=[DataRequired()])
    # TODO implement enum restriction
    genres = SelectMultipleField(
        "genres", validators=[DataRequired()], choices=Genre.genre_choice()
    )
    facebook_link = StringField(
        "facebook_link", validators=[URL(message="Facebook Link"), DataRequired()]
    )
    website = StringField("website")
    seeking_talent = BooleanField("seeking_talent")
    seeking_description = StringField("seeking_description")


class ArtistForm(Form):
    name = StringField("name", validators=[DataRequired()])
    city = StringField("city", validators=[DataRequired()])
    state = SelectField(
        "state", validators=[DataRequired()], choices=State.state_choice()
    )
    phone = StringField("phone", validators=[DataRequired()])
    image_link = StringField("image_link", validators=[DataRequired()])
    genres = SelectMultipleField(
        "genres", validators=[DataRequired()], choices=Genre.genre_choice()
    )
    facebook_link = StringField(
        # TODO implement enum restriction
        "facebook_link",
        validators=[URL(message="Facebook Link"), DataRequired()],
    )
    artist_website = StringField("artist_website")
    seeking_venue = BooleanField("seeking_venue")
    seeking_description = StringField("seeking_description")
