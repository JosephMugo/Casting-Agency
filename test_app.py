import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor

password = os.environ.get('DATABASEPASS')
assistant = os.environ.get('ASSISTANT_TOKEN')
director = os.environ.get('DIRECTOR_TOKEN')
executive = os.environ.get('EXECUTIVE_TOKEN')

if not password:
    raise ValueError('Missing database password')

# if not assistant:
#     raise ValueError('Missing assistant token')

# if not director:
#     raise ValueError('Missing director token')

if not executive:
    raise ValueError('Missing executive token')

class CastingAgencyTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'castingagency_test'
        # self.database_path = 'postgresql://postgres:' + password + '@localhost:5432/' + self.database_name
        self.database_path = "postgresql://postgres:{}@{}/{}".format(password, 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()
    
    def tearDown(self):
        pass

    # GET /movies
        # pass
    # movie record has to exist in database for test to pass
    def test_get_movies(self):
        res = self.client().get('/movies', headers={'Authorization': f'Bearer {executive}'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['movies']))
        # fail - no auth
    def test_fail_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
    # POST /movies
        # pass
        # fail


    # GET /actors
        # pass
        # fail


    # POST /actors
        # pass
        # fail


    # PATCH /actors/<int:actor_id>
        # pass
        # fail


    # DELETE /actors/<int:actor_id>
        # pass
        # fail
    

if __name__ == "__main__":
    unittest.main()