# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
import json
import sys
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from models import db, Venue, Artist, Show


# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#
# TODO: connect to a local postgresql database
# completed


def initialize_app():
    app = Flask(__name__)
    moment = Moment(app)
    app.config.from_object("config")
    db.init_app(app)
    migrate = Migrate(app, db)
    return app


app = initialize_app()


# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#
# TODO: implement any missing fields, as a database migration using Flask-Migrate
# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
# completed in models.py file

with app.app_context():
    db.create_all()


# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#
def format_datetime(value, format="medium"):
    date = dateutil.parser.parse(value)
    if format == "full":
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == "medium":
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale="en")


app.jinja_env.filters["datetime"] = format_datetime


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#
@app.route("/")
def index():
    return render_template("pages/home.html")


# ----------------------------------------------------------------------------#
#  All Venues
#  ----------------------------------------------------------------
@app.route("/venues")
def venues():
    # TODO: replace with real venues data.
    #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.

    # Querying all the Venues and Shows
    query_all_venues = Venue.query.all()
    query_all_shows = Show.query.all()

    """function for counting all the upcoming shows
       for the particular venue_id. It takes in venue_id as parameter
       and returns no. of shows or count
    """

    def upcoming_show(venue_id):
        count = 0
        for show in query_all_shows:
            if show.venue_id == venue_id:
                if show.start_time > datetime.now():
                    count += 1
        return count

    """Here we create a dictionary to find all the distinct cities and states"""
    venue_dict = {}
    for record in query_all_venues:
        regionkey = record.city + "-" + record.state
        """ The following if statement checks 
            if a particular city-state exists in the venue_dict
            and if it exists the we append the venue from the same city-state
            to the venues list/array"""
        if regionkey in venue_dict:
            venue_dict[regionkey]["venues"].append(
                {
                    "id": record.id,
                    "name": record.name,
                    # here for the num_upcoming_shows we get the count from the upcoming_show function
                    "num_upcoming_shows": upcoming_show(record.id),
                }
            )
            """Since the city-state from the record doesn't exist in the venue_dict
               we add a new key-value pair in the dict for the new city-state"""
        else:
            venue_dict[regionkey] = {
                "city": record.city,
                "state": record.state,
                "venues": [
                    {
                        "id": record.id,
                        "name": record.name,
                        "num_upcoming_shows": upcoming_show(record.id),
                    }
                ],
            }
    # now we create a list/array of the venue_dict values
    # to be sent to the html page
    venue = list(venue_dict.values())
    return render_template("pages/venues.html", areas=venue)


# ----------------------------------------------------------------------------#
# Venue Search
# ----------------------------------------------------------------------------#
@app.route("/venues/search", methods=["POST"])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

    """
    request search term and make all the text lower and
    trim all its extra whitespaces
    """
    venue_to_search = request.form.get("search_term")
    venue_to_search = venue_to_search.lower().lstrip().rstrip()
    """
    compare the search_term with name of all the Venue
    with func.lower(Venue.name) and returns a list for all
    venues with similar string
    """
    venue_search_list = Venue.query.filter(
        func.lower(Venue.name).contains(venue_to_search)
    )

    response = {"count": venue_search_list.count(), "data": venue_search_list}
    return render_template(
        "pages/search_venues.html",
        results=response,
        search_term=request.form.get("search_term"),
    )


# ----------------------------------------------------------------------------#
# Venue page
# ----------------------------------------------------------------------------#
@app.route("/venues/<int:venue_id>")
def show_venue(venue_id):
    # TODO: replace with real venue data from the venues table, using venue_id
    # create 2 lists for past and upcoming shows

    # querying the venues for the venue_id
    venue = Venue.query.filter(Venue.id == venue_id).first()
    # list for past and upcoming shows
    past_shows = []
    upcoming_shows = []
    # querying the shows for the venue_id provided
    shows = Show.query.filter(Show.venue_id == venue_id).all()
    for show in shows:
        # getting the artists' shows for the venue_id
        # artist = show.artist_id
        # comparing with the start_time with current_time for maintaining
        # upcoming and past shows
        if show.start_time > datetime.now():
            upcoming_shows.append(
                {
                    "artist_id": show.artist.id,
                    "artist_name": show.artist.name,
                    "artist_image_link": show.artist.image_link,
                    "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M"),
                }
            )
        else:
            past_shows.append(
                {
                    "artist_id": show.artist.id,
                    "artist_name": show.artist.name,
                    "artist_image_link": show.artist.image_link,
                    "start_time": show.start_time.strftime("%Y/%m/%d, %H:%M"),
                }
            )

    # enlisting all the venue details for the '/venue/venue_id' endpoint
    venue_details = {
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }
    return render_template("pages/show_venue.html", venue=venue_details)


# ----------------------------------------------------------------#
#  Create Venue
# ----------------------------------------------------------------#
@app.route("/venues/create", methods=["GET", "POST"])
def create_venue_submission():
    form = VenueForm(request.form)
    if request.method == "POST":
        if form.validate():
            try:
                # requesting the form data
                # assigning and accessing the values from the form data
                name = form.name.data
                city = form.city.data
                state = form.state.data
                address = form.address.data
                phone = int(form.phone.data)
                image_link = form.image_link.data
                genres = form.genres.data
                facebook_link = form.facebook_link.data
                website = form.website.data
                seeking_talent = form.seeking_talent.data
                seeking_description = form.seeking_description.data

                # initializing new Venue object to be added to the database
                new_venue = Venue(
                    name=name,
                    city=city,
                    state=state,
                    address=address,
                    phone=phone,
                    image_link=image_link,
                    genres=genres,
                    facebook_link=facebook_link,
                    website=website,
                    seeking_talent=seeking_talent,
                    seeking_description=seeking_description,
                )

                # adding the new venue object to database
                db.session.add(new_venue)
                db.session.commit()
                flash("Venue " + request.form["name"] + " was successfully listed!")
            except:
                # if adding to the database failed, rollback the changes
                db.session.rollback()
                print(sys.exc_info)
                print("There was an error")
                flash("Venue " + request.form["name"] + " was not listed!")
            finally:
                db.session.close()
            return render_template("pages/home.html")
        else:
            for error_field, error_message in form.errors.items():
                flash(f"{error_field} - {error_message}")
    return render_template("forms/new_venue.html", form=form)


# ----------------------------------------------------------------------------#
# Edit Venue
# ----------------------------------------------------------------------------#
# querying both get and post method here
@app.route("/venues/<int:venue_id>/edit", methods=["GET", "POST"])
def edit_venue_submission(venue_id):
    # accessing the venue data for the given id
    edit_venue = Venue.query.get(venue_id)
    # get_form to render the edit form and to prepopulate
    get_form = VenueForm(obj=edit_venue)
    # post_form to change the values
    post_form = VenueForm(request.form)
    if request.method == "POST":
        try:
            edit_venue.name = post_form.name.data
            edit_venue.city = post_form.city.data
            edit_venue.state = post_form.state.data
            edit_venue.address = post_form.address.data
            edit_venue.phone = int(post_form.phone.data)
            edit_venue.image_link = post_form.image_link.data
            edit_venue.genres = post_form.genres.data
            edit_venue.facebook_link = post_form.facebook_link.data
            edit_venue.website = post_form.website.data
            edit_venue.seeking_talent = post_form.seeking_talent.data
            edit_venue.seeking_description = post_form.seeking_description.data
            db.session.add(edit_venue)
            db.session.commit()
            flash(f"Changes have been made to the {edit_venue.name}")
        except:
            db.session.rollback()
            print(sys.int_info)
            flash("There was some error!")
        finally:
            db.session.close()
        # TODO: take values from the form submitted, and update existing
        # venue record with ID <venue_id> using the new attributes
        return redirect(url_for("show_venue", venue_id=venue_id))
    return render_template("forms/edit_venue.html", form=get_form, venue=edit_venue)


# ----------------------------------------------------------------------------#
# Delete Venue
# ----------------------------------------------------------------------------#
# delete a particular venue using get method
@app.route("/venues/<venue_id>/delete", methods=["GET"])
def delete_venue(venue_id):
    # query the venue using venue_id
    venue = Venue.query.get(venue_id)
    try:
        # delete venue from database
        # since cascade is in place it will delete its entry from every table (Venue and Show)
        db.session.delete(venue)
        db.session.commit()
        flash(f"Venue {venue.name} deleted")
        return render_template("pages/home.html")
    except:
        db.session.rollback()
        print(sys.exc_info)
        flash("Venue cannot be deleted now!")
    finally:
        db.session.close()
    return redirect(url_for("venues"))


# ----------------------------------------------------------------#
#  All Artists
# ----------------------------------------------------------------#
@app.route("/artists")
def artists():
    # TODO: replace with real data returned from querying the database
    # query all the artist
    artist_list = Artist.query.order_by(Artist.id).all()
    data = []
    for artist in artist_list:
        # adding the artist object to a list named data
        data.append({"id": artist.id, "name": artist.name})
    return render_template("pages/artists.html", artists=data)


# ----------------------------------------------------------------#
#  Artists search
# ----------------------------------------------------------------#
@app.route("/artists/search", methods=["POST"])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    # completed

    """
    request search term and make all the text lower and
    trim all its extra whitespaces
    """
    artist_to_search = request.form.get("search_term")
    artist_to_search = artist_to_search.lower().lstrip().rstrip()
    """
    compare the search_term with name of all the Artist
    with func.lower(Artist.name) and returns a list for all
    Artist with similar string
    """
    artist_search_list = Artist.query.filter(
        func.lower(Artist.name).contains(artist_to_search)
    )
    response = {"count": artist_search_list.count(), "data": artist_search_list}
    return render_template(
        "pages/search_artists.html",
        results=response,
        search_term=request.form.get("search_term"),
    )


# ----------------------------------------------------------------#
#  Artist page
# ----------------------------------------------------------------#
@app.route("/artists/<int:artist_id>")
def show_artist(artist_id):
    # querying the artist table for the artist_id
    artist = Artist.query.filter(Artist.id == artist_id).first()
    # querying the shows for the artist_id provided
    shows = Show.query.filter(Show.artist_id == artist_id).all()
    # list for past and upcoming shows
    upcoming_venue_for_band = []
    past_venue_for_band = []

    for show in shows:
        # getting the artists' shows for the venue_id
        venue = Venue.query.get(show.venue_id)
        # comparing with the start_time with current_time for maintaining
        # upcoming and past shows
        if show.start_time > datetime.now():
            upcoming_venue_for_band.append(
                {
                    "venue_id": venue.id,
                    "venue_name": venue.name,
                    "venue_image_link": venue.image_link,
                    "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M"),
                }
            )
        else:
            past_venue_for_band.append(
                {
                    "venue_id": venue.id,
                    "venue_name": venue.name,
                    "venue_image_link": venue.image_link,
                    "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M"),
                }
            )

    # shows the artist page with the given artist_id
    # TODO: replace with real artist data from the artist table, using artist_id
    # enlisting all the venue details for the '/venue/venue_id' endpoint
    artist_details = {
        "id": artist.id,
        "name": artist.name,
        "genres": artist.genres,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "seeking_venue": artist.seeking_venue,
        "image_link": artist.image_link,
        "website": artist.artist_website,
        "facebook_link": artist.facebook_link,
        "past_shows": past_venue_for_band,
        "upcoming_shows": upcoming_venue_for_band,
        "past_shows_count": len(past_venue_for_band),
        "upcoming_shows_count": len(upcoming_venue_for_band),
    }
    return render_template("pages/show_artist.html", artist=artist_details)


# ----------------------------------------------------------------#
#  Edit Artist
# ----------------------------------------------------------------#
#     # TODO: populate form with fields from artist with ID <artist_id>
#       TODO: take values from the form submitted, and update existing
#             artist record with ID <artist_id> using the new attributes
# completed
# referenced from https://www.reddit.com/r/flask/comments/m5tgra/prepopulate_edit_form_from_model_with/ for "obj=""
@app.route("/artists/<int:artist_id>/edit", methods=["GET", "POST"])
def edit_artist_submission(artist_id):
    # query artist for the given artist_id
    edit_artist = Artist.query.get(artist_id)

    # using "obj=" to prepopulate the form fields
    get_artist_form = ArtistForm(obj=edit_artist)
    # requesting artist form field data
    post_artist_form = ArtistForm(request.form)
    if request.method == "POST":
        try:
            # update artist details
            edit_artist.name = post_artist_form.name.data
            edit_artist.city = post_artist_form.city.data
            edit_artist.state = post_artist_form.state.data
            edit_artist.phone = post_artist_form.phone.data
            edit_artist.image_link = post_artist_form.image_link.data
            edit_artist.genres = post_artist_form.genres.data
            edit_artist.facebook_link = post_artist_form.facebook_link.data
            edit_artist.artist_website = post_artist_form.artist_website.data
            edit_artist.seeking_venue = post_artist_form.seeking_venue.data
            edit_artist.seeking_description = post_artist_form.seeking_description.data
            db.session.add(edit_artist)
            db.session.commit()
            flash(f"Artist { edit_artist.name } has been edited!")
        except:
            db.session.rollback()
            print(sys.int_info)
            flash("Error in editing artist!")
        finally:
            db.session.close()
        return redirect(url_for("show_artist", artist_id=artist_id))
    return render_template(
        "forms/edit_artist.html", form=get_artist_form, artist=edit_artist
    )


# ----------------------------------------------------------------#
#  Create Artist
# ----------------------------------------------------------------#
@app.route("/artists/create", methods=["GET", "POST"])
def create_artist_submission():
    form = ArtistForm(request.form)
    if request.method == "POST":
        if form.validate():
            try:
                name = form.name.data
                city = form.city.data
                state = form.state.data
                phone = int(form.phone.data)
                genres = form.genres.data
                image_link = form.image_link.data
                facebook_link = form.facebook_link.data
                website = form.artist_website.data
                seeking_venue = form.seeking_venue.data
                seeking_description = form.seeking_description.data

                new_artist = Artist(
                    name=name,
                    city=city,
                    state=state,
                    phone=phone,
                    genres=genres,
                    image_link=image_link,
                    facebook_link=facebook_link,
                    artist_website=website,
                    seeking_venue=seeking_venue,
                    seeking_description=seeking_description,
                )
                db.session.add(new_artist)
                db.session.commit()
                flash("Artist " + request.form["name"] + " was successfully listed!")
            except:
                db.session.rollback()
                print(sys.int_info)
                flash("Artist " + request.form["name"] + " was not listed!")
            finally:
                db.session.close()
            return render_template("pages/home.html")
        else:
            for error_field, error_message in form.errors.items():
                flash(f"{error_field} - {error_message}")
    return render_template("forms/new_artist.html", form=form)

    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    # on successful db insert, flash success
    flash("Artist " + request.form["name"] + " was successfully listed!")
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')


# ----------------------------------------------------------------#
#  All Shows
# ----------------------------------------------------------------#
@app.route("/shows")
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    # completed

    # query all the shows details
    shows = Show.query.all()
    show_data = []
    for show in shows:
        print(show)
        # append show data to an list
        # referenced from https://knowledge.udacity.com/questions/510080#510112
        show_data.append(
            {
                "venue_id": show.venue_id,
                "venue_name": show.venue.name,
                "artist_id": show.artist_id,
                "artist_name": show.artist.name,
                "artist_image_link": show.artist.image_link,
                "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M"),
            }
        )
    return render_template("pages/shows.html", shows=show_data)


# ---------------------------------------------------------#
# Create Shows
# ---------------------------------------------------------#
@app.route("/shows/create", methods=["GET", "POST"])
# applying both get and post method together
def create_show():
    form = ShowForm(request.form)
    if request.method == "POST":
        if form.validate():
            try:
                # accessing values from show form
                artist_id = form.artist_id.data
                venue_id = form.venue_id.data
                start_time = form.start_time.data
                # print(start_time)
                new_show = Show(
                    artist_id=artist_id, venue_id=venue_id, start_time=start_time
                )
                db.session.add(new_show)
                db.session.commit()
                flash("Show was successfully listed.")
            except:
                db.session.rollback()
                print(sys.int_info)
                flash("An error occurred. Show could not be listed.")
            finally:
                db.session.close()
            return render_template("pages/home.html")
        else:
            for error_field, error_message in form.errors.items():
                flash(f"{error_field} - {error_message}")

    return render_template("forms/new_show.html", form=form)


# called to create new shows in the db, upon submitting new show listing form
# TODO: insert form data as a new Show record in the db, instead
# on successful db insert, flash success
# TODO: on unsuccessful db insert, flash an error instead.
# e.g., flash('An error occurred. Show could not be listed.')
# see: http://flask.pocoo.org/docs/1.0/patterns/flashing/


# ----------------------------------------------------------------------------#
# Error handlers
# ----------------------------------------------------------------------------#
@app.errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("errors/500.html"), 500


if not app.debug:
    file_handler = FileHandler("error.log")
    file_handler.setFormatter(
        Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]")
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info("errors")


# ----------------------------------------------------------------------------#
# Launch App.
# ----------------------------------------------------------------------------#
# Default port:
if __name__ == "__main__":
    app.run()
# Or specify port manually:
"""
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
"""
