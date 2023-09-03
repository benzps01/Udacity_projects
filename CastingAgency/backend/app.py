from flask import Flask, request, abort, jsonify
import json
import os, random, sys
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, setup_db, Movie, Actor


def create_app(database_uri="", test_config=None):
    app = Flask(__name__)
    if database_uri:
        setup_db(app, database_uri)
    else:
        setup_db(app)
    CORS(app)
    return app


app = create_app()


@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add(
        "Access-Control-Allow-Headers", "Content-Type, Authorization, true"
    )
    response.headers.add(
        "Access-Control-Allow-Methods", "GET,POST,PATCH,DELETE,OPTIONS"
    )
    return response


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


@app.route("/movies", methods=["GET", "POST"])
def add_movies():
    try:
        if request.method == "POST":
            title = request.get_json().get("title")
            release_date = request.get_json().get("release_date")
            genre = request.get_json().get("genre")
            actor_id = request.get_json().get("actor_id")
            ## actorid check
            check_actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            if check_actor.id != actor_id:
                abort(404)
            new_movie = Movie(
                title=title, release_date=release_date, genre=genre, actor_id=actor_id
            )
            new_movie.insert()
            return jsonify({"success": True, "movie_dict": get_movies()})
        elif request.method == "GET":
            return get_movies()
    except:
        abort(400)


@app.route("/movies/<int:movie_id>", methods=["DELETE"])
def delete_movie(movie_id):
    try:
        movie_to_delete = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if movie_to_delete is None:
            abort(404)
        temp = movie_to_delete.title
        movie_to_delete.delete()
        return jsonify(
            {
                "success": True,
                "movie_dict": get_movies(),
                "deleted_movie_title": temp,
            }
        )
    except:
        abort(400)


@app.route("/movies/<int:movie_id>", methods=["PATCH"])
def update_movie(movie_id):
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
        return jsonify({"success": True, "movie_dict": get_movies()})
    except:
        abort(400)


@app.route("/actors", methods=["GET", "POST"])
def add_actors():
    try:
        if request.method == "POST":
            name = request.get_json().get("name")
            age = request.get_json().get("age")
            gender = request.get_json().get("gender")
            new_actor = Actor(name=name, age=age, gender=gender)
            new_actor.insert()
            return jsonify({"success": True, "actors_dict": get_actors()})
        elif request.method == "GET":
            return get_actors()
    except:
        abort(400)


@app.route("/actors/<int:actor_id>", methods=["DELETE"])
def delete_an_actor(actor_id):
    try:
        actor_to_delete = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor_to_delete is None:
            abort(404)
        temp = actor_to_delete.name
        actor_to_delete.delete()
        return jsonify(
            {"success": True, "actor_dict": get_actors(), "deleted_actor_name": temp}
        )
    except:
        abort(400)


@app.route("/actors/<int:actor_id>", methods=["PATCH"])
def update_actor_details(actor_id):
    try:
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
        return jsonify({"success": True, "actor_dict": get_actors()})
    except:
        abort(400)


if __name__ == "__main__":
    app.run(debug=True)
