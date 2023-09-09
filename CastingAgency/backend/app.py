from flask import Flask, request, abort, jsonify
import json
import os, random, sys
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_cors import CORS
from models import db, setup_db, Movie, Actor
from auth import AuthError, requires_auth


# -----------------------------------------------------------------------------------------------!
# Create App with database URI
# -----------------------------------------------------------------------------------------------!
def create_app(database_uri="", test_config=None):
    app = Flask(__name__)
    if database_uri:
        setup_db(app, database_uri)
    else:
        setup_db(app)
    CORS(app)

    # -----------------------------------------------------------------------------------------------!
    # CORS is defined above
    # Access-conrols for origins, headers, methods
    # -----------------------------------------------------------------------------------------------!
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization,True"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,POST,PATCH,DELETE,OPTIONS"
        )
        return response

    # -----------------------------------------------------------------------------------------------!
    # This is a test point to check if the app works
    # -----------------------------------------------------------------------------------------------!
    @app.route("/", methods=["GET"])
    def test_point():
        return jsonify({"success": True})

    # -----------------------------------------------------------------------------------------------!
    # This method is used to get movie list as a list
    # -----------------------------------------------------------------------------------------------!
    def get_movies():
        movie_list = []
        all_movies = Movie.query.all()
        movie_list = [movie.format() for movie in all_movies]
        return movie_list

    # -----------------------------------------------------------------------------------------------!
    # This method is used to get actor list as a list
    # -----------------------------------------------------------------------------------------------!
    def get_actors():
        actor_list = []
        all_actors = Actor.query.all()
        actor_list = [actor.format() for actor in all_actors]
        return actor_list

    # -----------------------------------------------------------------------------------------------!
    # Route: GET
    # Permission required: GET:MOVIES
    # This route is used to get all the movie data... get_movies() is defined above
    # -----------------------------------------------------------------------------------------------!
    @app.route("/movies", methods=["GET"])
    @requires_auth("get:movies")
    def get_movie(payload):
        try:
            return jsonify({"success": True, "movies_dict": get_movies()})
        except:
            abort(400)

    # -----------------------------------------------------------------------------------------------!
    # Route: POST
    # Permission required: POST:MOVIES
    # This route is used to add new movie
    # -----------------------------------------------------------------------------------------------!
    @app.route("/movies", methods=["POST"])
    @requires_auth("post:movies")
    def add_movie(payload):
        title = request.get_json().get("title") or None
        release_date = request.get_json().get("release_date")
        genre = request.get_json().get("genre")
        actor_id = request.get_json().get("actor_id")
        ## actorid check
        if title is None:
            abort(400)
        if release_date is None:
            abort(400)
        if genre is None:
            abort(400)
        if actor_id is None:
            abort(400)
        check_actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if check_actor is None:
            abort(404)
        try:
            new_movie = Movie(
                title=title, release_date=release_date, genre=genre, actor_id=actor_id
            )
            new_movie.insert()
            return (
                jsonify(
                    {
                        "success": True,
                        "movies_dict": get_movies(),
                        "total_movies": len(Movie.query.all()),
                    }
                ),
                200,
            )
        except:
            raise abort(400)

    # -----------------------------------------------------------------------------------------------!
    # Route: DELETE
    # Permission required: DELETE:MOVIES
    # This route is used to delete a movie
    # -----------------------------------------------------------------------------------------------!
    @app.route("/movies/<int:movie_id>", methods=["DELETE"])
    @requires_auth("delete:movies")
    def delete_movie(payload, movie_id):
        movie_to_delete = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie_to_delete is None:
            abort(404)
        try:
            temp = movie_to_delete.title
            movie_to_delete.delete()
            return (
                jsonify(
                    {
                        "success": True,
                        "movies_dict": get_movies(),
                        "deleted_movie_title": temp,
                    }
                ),
                200,
            )
        except:
            abort(400)

    # -----------------------------------------------------------------------------------------------!
    # Route: PATCH
    # Permission required: PATCH:MOVIES
    # This route is used to update a movie
    # -----------------------------------------------------------------------------------------------!
    @app.route("/movies/<int:movie_id>", methods=["PATCH"])
    @requires_auth("patch:movies")
    def update_movie(payload, movie_id):
        movie_to_update = Movie.query.filter(Movie.id == movie_id).one_or_none()
        print(movie_to_update)
        if movie_to_update is None:
            abort(404)
        title = request.get_json().get("title")
        release_date = request.get_json().get("release_date")
        genre = request.get_json().get("genre")
        actor_id = request.get_json().get("actor_id")
        # -----------------------------------------------------------------------------------------------!
        # This section is used to check if a single data is to be updated or multiple data
        # -----------------------------------------------------------------------------------------------!
        if title is not None:
            movie_to_update.title = title
        else:
            abort(400)
        if release_date is not None:
            movie_to_update.release_date = release_date
        else:
            abort(400)
        if genre is not None:
            movie_to_update.genre = genre
        else:
            abort(400)
        if actor_id is not None:
            movie_to_update.actor_id = actor_id
        else:
            abort(400)
        try:
            movie_to_update.update()
            return (
                jsonify(
                    {
                        "success": True,
                        "movies_dict": [movie.format() for movie in Movie.query.all()],
                    }
                ),
                200,
            )
        except:
            abort(400)

    # -----------------------------------------------------------------------------------------------!
    # Route: GET
    # Permission required: GET:ACTORS
    # This route is used to get actors.. get_actors() is defined above
    # -----------------------------------------------------------------------------------------------!
    @app.route("/actors", methods=["GET"])
    @requires_auth("get:actors")
    def get_actor(payload):
        try:
            return jsonify({"success": True, "actors_dict": get_actors()})
        except:
            abort(400)

    # -----------------------------------------------------------------------------------------------!
    # Route: POST
    # Permission required: POST:ACTORS
    # This route is used to add new actors
    # -----------------------------------------------------------------------------------------------!
    @app.route("/actors", methods=["POST"])
    @requires_auth("post:actors")
    def add_actor(payload):
        name = request.get_json().get("name")
        age = request.get_json().get("age")
        gender = request.get_json().get("gender")
        if name is None:
            abort(400)
        if age is None:
            abort(400)
        if gender is None:
            abort(400)
        try:
            new_actor = Actor(name=name, age=age, gender=gender)
            new_actor.insert()
            return jsonify({"success": True, "actors_dict": get_actors()}), 200
        except:
            abort(400)

    # -----------------------------------------------------------------------------------------------!
    # Route: DELETE
    # Permission required: DELETE:ACTORS
    # This route is used to delete an actor
    # -----------------------------------------------------------------------------------------------!
    @app.route("/actors/<int:actor_id>", methods=["DELETE"])
    @requires_auth("delete:actors")
    def delete_an_actor(payload, actor_id):
        actor_to_delete = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor_to_delete is None:
            abort(404)
        try:
            temp = actor_to_delete.name
            actor_to_delete.delete()
            return (
                jsonify(
                    {
                        "success": True,
                        "actors_dict": get_actors(),
                        "deleted_actor_name": temp,
                    }
                ),
                200,
            )
        except:
            abort(403)

    # -----------------------------------------------------------------------------------------------!
    # Route: PATCH
    # Permission required: PATCH:ACTORS
    # This route is used to update an actor
    # -----------------------------------------------------------------------------------------------!
    @app.route("/actors/<int:actor_id>", methods=["PATCH"])
    @requires_auth("patch:actors")
    def update_actor_details(payload, actor_id):
        actor_to_be_updated = Actor.query.get(actor_id)
        if actor_to_be_updated is None:
            abort(404)
        name = request.get_json().get("name")
        age = request.get_json().get("age")
        gender = request.get_json().get("gender")
        # -----------------------------------------------------------------------------------------------!
        # This section is used to check if a single data is to be updated or multiple data
        # -----------------------------------------------------------------------------------------------!
        if name is not None:
            actor_to_be_updated.name = name
        else:
            abort(400)
        if age is not None:
            actor_to_be_updated.age = age
        else:
            abort(400)
        if gender is not None:
            actor_to_be_updated.gender = gender
        else:
            abort(400)
        try:
            actor_to_be_updated.update()
            return jsonify({"success": True, "actors_dict": get_actors()}), 200
        except:
            abort(403)

    # -----------------------------------------------------------------------------------------------!
    # This is an helper method to raise error if error is unreachable
    # -----------------------------------------------------------------------------------------------!
    class RequestError(Exception):
        def __init__(self, status):
            self.status = status

        def __str__(self):
            return repr(self.status)

    # -----------------------------------------------------------------------------------------------!
    # Error Handlers
    # This is 400 bad request error
    # -----------------------------------------------------------------------------------------------!
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "Bad Request"}), 400

    # -----------------------------------------------------------------------------------------------!
    # Error Handlers
    # This is 401 unauthorized error
    # -----------------------------------------------------------------------------------------------!
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({"success": False, "error": 401, "message": "Unauthorized"}), 401

    # -----------------------------------------------------------------------------------------------!
    # Error Handlers
    # This is 403 forbidden error
    # -----------------------------------------------------------------------------------------------!
    @app.errorhandler(403)
    def forbidden(error):
        return (
            jsonify({"success": False, "error": 403, "message": "forbidden to access"}),
            403,
        )

    # -----------------------------------------------------------------------------------------------!
    # Error Handlers
    # This is 404 not_found error
    # -----------------------------------------------------------------------------------------------!
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 404,
                    "message": "Requested Resource Not Found",
                }
            ),
            404,
        )

    # -----------------------------------------------------------------------------------------------!
    # Error Handlers
    # This is 422 unprocessable error
    # -----------------------------------------------------------------------------------------------!
    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    # -----------------------------------------------------------------------------------------------!
    # Error Handlers
    # This is 500 server_error error
    # -----------------------------------------------------------------------------------------------!
    @app.errorhandler(500)
    def server_error(error):
        return (
            jsonify(
                {"success": False, "error": 500, "message": "Internal Server Error"}
            ),
            500,
        )

    # -----------------------------------------------------------------------------------------------!
    # Error Handlers
    # This handles the permission or Authentication errors
    # -----------------------------------------------------------------------------------------------!
    @app.errorhandler(AuthError)
    def auth_error_handler(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
