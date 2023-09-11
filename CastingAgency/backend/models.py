import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from sqlalchemy.dialects import postgresql
from flask_migrate import Migrate
import json

# -----------------------------------------------------------------------------------------------!
# This is the database_path definition 1 - local database, 2 - render database
# -----------------------------------------------------------------------------------------------!
load_dotenv()
# database_path = f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}/{os.getenv("DB_NAME")}'
database_path = "postgresql://casts:0Pi3F0CqpbvvW1gto89OG51CoW2bXLA5@dpg-cjvmv2p5mpss73912h9g-a/castingagency_kuu2"
db = SQLAlchemy()


# -----------------------------------------------------------------------------------------------!
# This method is used to setup database
# -----------------------------------------------------------------------------------------------!
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    with app.app_context():
        db.create_all()


# -----------------------------------------------------------------------------------------------!
# The tables are setup as ONE to MANY relationships
# This is Movie table
# Attributes - id
#            - title
#            - release_date
#            - genre
#            - actor_id
# -----------------------------------------------------------------------------------------------!
class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    release_date = db.Column(db.String, nullable=False)
    genre = db.Column(db.String(20), nullable=False)
    actor_id = db.Column(db.Integer, db.ForeignKey("actors.id", ondelete="CASCADE"))

    def __init__(self, title, release_date, genre, actor_id):
        self.title = title
        self.release_date = release_date
        self.genre = genre
        self.actor_id = actor_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "genre": self.genre,
            "actor_id": self.actor_id,
        }


# -----------------------------------------------------------------------------------------------!
# This is Actor table
# Attributes - id
#            - name
#            - age
#            - gender
# -----------------------------------------------------------------------------------------------!
class Actor(db.Model):
    __tablename__ = "actors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    movies = db.relationship(
        "Movie", backref="actor", cascade="all, delete-orphan", passive_deletes=True
    )

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
        }
