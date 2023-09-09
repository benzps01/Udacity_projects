import os, sys
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Movie, Actor, db
from app import create_app
from dotenv import load_dotenv

# -----------------------------------------------------------------------------------------------!
# getting all the necessary details from .env file
# -----------------------------------------------------------------------------------------------!
load_dotenv()
database = os.getenv("TEST_DB_NAME")
password = os.getenv("TEST_DB_PASSWORD")
host = os.getenv("TEST_DB_HOST")
user = os.getenv("TEST_DB_USER")
cast_assist = os.getenv("CAST_ASSISTANT")
cast_direct = os.getenv("CAST_DIRECTOR")
exec_prod = os.getenv("EXEC_PRODUCER")


# -----------------------------------------------------------------------------------------------!
# actor, movie and movie_with_non_existent_actor_id json data
# -----------------------------------------------------------------------------------------------!
actor = {"name": "Benson", "age": 23, "gender": "male"}

movie = {
    "title": "Interstellar",
    "release_date": "20/04/1998",
    "genre": "Sci-Fi",
    "actor_id": 1,
}

movie_non = {
    "title": "Interstellar",
    "release_date": "20/04/1998",
    "genre": "Sci-Fi",
    "actor_id": 10,
}


# -----------------------------------------------------------------------------------------------!
# Test Setup
# -----------------------------------------------------------------------------------------------!
class CastingAgencyTestCase(unittest.TestCase):
    def setUp(self):
        self.database_path = f"postgresql://{user}:{password}@{host}/{user}"
        self.app = create_app(self.database_path)
        self.client = self.app.test_client
        self.db = db
        with self.app.app_context():
            self.db.create_all()

    # -----------------------------------------------------------------------------------------------!
    # This is to check if user can post a new actor
    # -----------------------------------------------------------------------------------------------!
    def test_check_post_actor(self):
        res = self.client().post(
            "/actors",
            headers={"Authorization": "Bearer " + exec_prod},
            json=actor,
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actors_dict"])

    # -----------------------------------------------------------------------------------------------!
    # This is to check if user can post a new actor with no permissions
    # -----------------------------------------------------------------------------------------------!
    def test_check_post_actor_with_no_permission(self):
        res = self.client().post(
            "/actors",
            headers={"Authorization": "Bearer " + cast_assist},
            json=actor,
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)

    # -----------------------------------------------------------------------------------------------!
    # This is to check if user can post a new actor with empty json file
    # -----------------------------------------------------------------------------------------------!
    def test_check_post_actor_with_no_data(self):
        res = self.client().post(
            "/actors", headers={"Authorization": "Bearer " + exec_prod}, json={}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)

    # -----------------------------------------------------------------------------------------------!
    # This is to check if user can post a new movie
    # -----------------------------------------------------------------------------------------------!
    def test_check_post_movie(self):
        res = self.client().post(
            "/movies",
            headers={"Authorization": "Bearer " + exec_prod},
            json=movie,
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movies_dict"], 1)

    # -----------------------------------------------------------------------------------------------!
    # This is to check if user can post a new movie with non existent actor id
    # -----------------------------------------------------------------------------------------------!
    def test_check_post_movie_with_non_existent_actorid(self):
        res = self.client().post(
            "/movies",
            headers={"Authorization": "Bearer " + exec_prod},
            json=movie_non,
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    # -----------------------------------------------------------------------------------------------!
    # This is to check if user can post a new movie with empty json file
    # -----------------------------------------------------------------------------------------------!
    def test_check_post_movie_with_no_data(self):
        res = self.client().post(
            "/movies",
            headers={"Authorization": "Bearer " + exec_prod},
            json={},
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"])

    # -----------------------------------------------------------------------------------------------!
    # This is to check if user can post a new movie with no permissions
    # -----------------------------------------------------------------------------------------------!
    def test_check_post_movie_with_no_permission(self):
        res = self.client().post(
            "/movies",
            headers={"Authorization": "Bearer " + cast_assist},
            json=movie,
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"])

    # -----------------------------------------------------------------------------------------------!
    # This is to check if user can get movie data
    # -----------------------------------------------------------------------------------------------!
    def test_check_get_movie(self):
        res = self.client().get(
            "/movies",
            headers={"Authorization": "Bearer " + exec_prod},
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movies_dict"])

    # -----------------------------------------------------------------------------------------------!
    # This is to check if user can get movie data without permission
    # -----------------------------------------------------------------------------------------------!
    def test_check_get_movie_without_permission(self):
        res = self.client().get("/movies")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["code"], "authorization_header_missing")

    # -----------------------------------------------------------------------------------------------!
    # This is to check if user can get actor data
    # -----------------------------------------------------------------------------------------------!
    def test_check_get_actor(self):
        res = self.client().get(
            "/actors",
            headers={"Authorization": "Bearer " + exec_prod},
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actors_dict"])

    # -----------------------------------------------------------------------------------------------!
    # This is to check if user can get actor data without permission
    # -----------------------------------------------------------------------------------------------!
    def test_check_get_actors_without_permission(self):
        res = self.client().get("/actors")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["code"], "authorization_header_missing")

    # -----------------------------------------------------------------------------------------------!
    # This is to check if user can update actor details
    # -----------------------------------------------------------------------------------------------!
    def test_check_patch_actor(self):
        res = self.client().patch(
            "/actors/1",
            headers={"Authorization": "Bearer " + exec_prod},
            json={"name": "Benson", "age": 26, "gender": "male"},
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actors_dict"])

    # -----------------------------------------------------------------------------------------------!
    # This is to check if user can update actor details with non existent actor id
    # -----------------------------------------------------------------------------------------------!
    def test_check_patch_actor_with_nonexistent_actorid(self):
        res = self.client().patch(
            "/actors/5",
            headers={"Authorization": "Bearer " + exec_prod},
            json={"name": "Benson", "age": 26, "gender": "male"},
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    # -----------------------------------------------------------------------------------------------!
    # This is to check if user can update actor details without permissions
    # -----------------------------------------------------------------------------------------------!
    def test_check_patch_actor_without_permission(self):
        res = self.client().patch(
            "/actors/1",
            headers={"Authorization": "Bearer " + cast_assist},
            json={"name": "Benson", "age": 26, "gender": "male"},
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"])

    # -----------------------------------------------------------------------------------------------!
    # This is to check if user can update movie details
    # -----------------------------------------------------------------------------------------------!
    def test_check_patch_movie(self):
        res = self.client().patch(
            "/movies/1",
            headers={"Authorization": "Bearer " + exec_prod},
            json=movie,
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movies_dict"])

    # -----------------------------------------------------------------------------------------------!
    # This is to check if user can update movie details with non existent movie id
    # -----------------------------------------------------------------------------------------------!
    def test_check_patch_movie_with_nonexistent_movieid(self):
        res = self.client().patch(
            "/movies/10",
            headers={"Authorization": "Bearer " + exec_prod},
            json=movie_non,
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    # -----------------------------------------------------------------------------------------------!
    # This is to check if user can update actor details without permission
    # -----------------------------------------------------------------------------------------------!
    def test_check_patch_movie_with_no_permission(self):
        res = self.client().patch(
            "/movies/1",
            headers={"Authorization": "Bearer " + cast_assist},
            json=movie,
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"])

    # -----------------------------------------------------------------------------------------------!
    # This is to check if user can delete movie
    # -----------------------------------------------------------------------------------------------!
    def test_check_delete_movie(self):
        res = self.client().delete(
            "/movies/1",
            headers={"Authorization": "Bearer " + exec_prod},
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["deleted_movie_title"])

    # -----------------------------------------------------------------------------------------------!
    # This is to check if user can delete movie with non existent movie id
    # -----------------------------------------------------------------------------------------------!
    def test_check_delete_movie_with_nonexistent_movieid(self):
        res = self.client().delete(
            "/movies/10",
            headers={"Authorization": "Bearer " + exec_prod},
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    # -----------------------------------------------------------------------------------------------!
    # This is to check if user can delete movie with no permissions
    # -----------------------------------------------------------------------------------------------!
    def test_check_delete_movie_no_permission(self):
        res = self.client().delete(
            "/movies/1",
            headers={"Authorization": "Bearer " + cast_direct},
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)

    # -----------------------------------------------------------------------------------------------!
    # This is to check if user can delete actor
    # -----------------------------------------------------------------------------------------------!
    def test_check_delete_actor(self):
        res = self.client().delete(
            "/actors/1",
            headers={"Authorization": "Bearer " + exec_prod},
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["deleted_actor_name"])

    # -----------------------------------------------------------------------------------------------!
    # This is to check if user can delete actor with non existent actor id
    # -----------------------------------------------------------------------------------------------!
    def test_check_delete_actor_with_nonexistent_actorid(self):
        res = self.client().delete(
            "/actors/10",
            headers={"Authorization": "Bearer " + exec_prod},
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    # -----------------------------------------------------------------------------------------------!
    # This is to check if user can delete actor without permissions
    # -----------------------------------------------------------------------------------------------!
    def test_check_delete_actor_no_permission(self):
        res = self.client().delete(
            "/actors/1",
            headers={"Authorization": "Bearer " + cast_assist},
        )

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)


if __name__ == "__main__":
    unittest.main()
