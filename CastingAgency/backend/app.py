from flask import Flask, request, abort, jsonify
import json
import os, random, sys
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, setup_db, Movie, Actor
from auth import AuthError, requires_auth


def create_app(database_uri="", test_config=None):
    app = Flask(__name__)
    if database_uri:
        setup_db(app, database_uri)
    else:
        setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,POST,PATCH,DELETE,OPTIONS"
        )
        return response

    return app


app = create_app()


@app.route("/", methods=["GET"])
def test_point():
    return "This is a test point"


def get_movies():
    movie_list = []
    all_movies = Movie.query.all()
    for movie in all_movies:
        movie_list.append(
            {
                "id": movie.id,
                "title": movie.title,
                "release_date": movie.release_date,
                "genre": movie.genre,
                "actor_id": movie.actor_id,
            }
        )
    return movie_list


def get_actors():
    actor_list = []
    all_actors = Actor.query.all()
    for actor in all_actors:
        actor_list.append(
            {
                "id": actor.id,
                "name": actor.name,
                "age": actor.age,
                "gender": actor.gender,
            }
        )
    return actor_list


@app.route("/movies", methods=["GET"])
@requires_auth("get:movies")
def get_movie(payload):
    try:
        return jsonify({"movies_dict": get_movies()}), 200
    except:
        abort(401)


@app.route("/movies", methods=["POST"])
@requires_auth("post:movies")
def add_movie(payload):
    try:
        title = request.get_json().get("title")
        release_date = request.get_json().get("release_date")
        genre = request.get_json().get("genre")
        actor_id = request.get_json().get("actor_id")
        ## actorid check
        check_actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if check_actor.id is None:
            abort(404)
        new_movie = Movie(
            title=title, release_date=release_date, genre=genre, actor_id=actor_id
        )
        new_movie.insert()
        return jsonify({"success": True, "movies_dict": get_movies()}), 200
    except:
        abort(403)


@app.route("/movies/<int:movie_id>", methods=["DELETE"])
@requires_auth("delete:movies")
def delete_movie(payload, movie_id):
    try:
        movie_to_delete = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie_to_delete is None:
            abort(404)
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
        abort(403)


@app.route("/movies/<int:movie_id>", methods=["PATCH"])
@requires_auth("patch:movies")
def update_movie(payload, movie_id):
    print(movie_id)
    try:
        movie_to_update = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie_to_update is None:
            abort(404)
        title = request.get_json().get("title")
        release_date = request.get_json().get("release_date")
        genre = request.get_json().get("genre")
        actor_id = request.get_json().get("actor_id")

        if title is not None:
            movie_to_update.title = title
        if release_date is not None:
            movie_to_update.release_date = release_date
        if genre is not None:
            movie_to_update.genre = genre
        if actor_id is not None:
            movie_to_update.actor_id = actor_id
        movie_to_update.update()
        return jsonify({"success": True, "movies_dict": get_movies()}), 200
    except:
        abort(403)


@app.route("/actors", methods=["GET"])
@requires_auth("get:actors")
def get_actor(payload):
    try:
        return get_actors()
    except:
        abort(401)


@app.route("/actors", methods=["POST"])
@requires_auth("post:actors")
def add_actor(payload):
    try:
        name = request.get_json().get("name")
        age = request.get_json().get("age")
        gender = request.get_json().get("gender")
        new_actor = Actor(name=name, age=age, gender=gender)
        new_actor.insert()
        return jsonify({"success": True, "actors_dict": get_actors()}), 200
    except:
        abort(401)


@app.route("/actors/<int:actor_id>", methods=["DELETE"])
@requires_auth("delete:actors")
def delete_an_actor(payload, actor_id):
    try:
        actor_to_delete = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor_to_delete is None:
            abort(404)
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


@app.route("/actors/<int:actor_id>", methods=["PATCH"])
@requires_auth("patch:actors")
def update_actor_details(payload, actor_id):
    try:
        print("This error", actor_id)
        actor_to_be_updated = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if actor_to_be_updated is None:
            abort(404)

        name = request.get_json().get("name")
        age = request.get_json().get("age")
        gender = request.get_json().get("gender")

        if name is not None:
            actor_to_be_updated.name = name
        if age is not None:
            actor_to_be_updated.age = age
        if gender is not None:
            actor_to_be_updated.gender = gender

        actor_to_be_updated.update()
        return jsonify({"success": True, "actors_dict": get_actors()}), 200
    except:
        abort(403)


@app.errorhandler(400)
def bad_request(error):
    return jsonify({"success": False, "error": 400, "message": "Bad Request"}), 400


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({"success": False, "error": 401, "message": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error):
    return (
        jsonify({"success": False, "error": 403, "message": "forbidden to access"}),
        403,
    )


@app.errorhandler(404)
def not_found(error):
    return (
        jsonify(
            {"success": False, "error": 404, "message": "Requested Resource Not Found"}
        ),
        404,
    )


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({"success": False, "error": 422, "message": "unprocessable"}), 422


@app.errorhandler(500)
def server_error(error):
    return (
        jsonify({"success": False, "error": 500, "message": "Internal Server Error"}),
        500,
    )


@app.errorhandler(AuthError)
def auth_error_handler(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


if __name__ == "__main__":
    app.run()
