import os, sys
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Movie, Actor, db
from app import create_app
from dotenv import load_dotenv

load_dotenv()
database = os.getenv("DB_NAME")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
cast_assist = os.getenv("CAST_ASSISTANT")
cast_direct = os.getenv("CAST_DIRECTOR")
exec_prod = os.getenv("EXEC_PRODUCER")


class CastingAgencyTestCase(unittest.TestCase):
    def setUp(self):
        self.database_path = f"postgresql://{user}:{password}@{host}/{database}"
        self.app = create_app(self.database_path)
        self.client = self.app.test_client

    def test_check_get_movie(self):
        res = self.client().get('/movies', headers={'Authorization': 'Bearer '+exec_prod})
        print(res.data)

        #data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["success"], True)
        #self.assertTrue(data["actors_dict"])


if __name__ == "__main__":
    unittest.main()
