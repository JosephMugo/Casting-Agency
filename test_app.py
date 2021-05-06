import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
import datetime

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
        
        self.new_movie = {
            "title": "Movie Test",
            "date": "4/4/2021"
        }

        self.new_actor = {
            "actor": "Test Actor",
            "age": 21,
            "gender": "male",
            "movie_id": 1
        }
    
    def tearDown(self):
        with self.app.app_context():
            self.db.drop_all()
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
    def test_create_movie(self):
        res = self.client().post('/movies', headers={'Authorization': f'Bearer {executive}'}, json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        # fail - no auth
    def test_fail_create_movie(self):
        res = self.client().post('/movies', json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
    # GET /actors
        # pass
    def test_get_actors(self):
        res = self.client().get('/actors', headers={'Authorization': f'Bearer {executive}'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['actors']))
        # fail - no auth
    def test_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    # POST /actors
        # pass
    def test_create_actors(self):
        res = self.client().post('/actors', headers={'Authorization': f'Bearer {executive}'}, json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        # fail - no auth
    def test_fail_create_actors(self):
        res = self.client().post('/actors', json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    # PATCH /actors/<int:actor_id>
        # pass
    def test_patch_actors(self):
        res = self.client().patch('/actors/1', headers={'Authorization': f'Bearer {executive}'}, json={"name": "New Name"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        # fail
    def test_fail_patch_actors(self):
        res = self.client().patch('/actors/1', json={"name": "New Name"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    # DELETE /actors/<int:actor_id>
        # pass
    def test_delete_actors(self):
        res = self.client().delete('/actors/1', headers={'Authorization': f'Bearer {executive}'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        # fail
    def test_fail_actors(self):
        res = self.client().delete('/actors/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

if __name__ == "__main__":
    unittest.main()