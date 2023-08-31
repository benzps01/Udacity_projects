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


@app.route("/")
def show_movies():
    return "This is a test point"


if __name__ == "__main__":
    app.run(debug=True)
