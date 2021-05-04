import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor

password = os.environ.get('DATABASEPASS')

class CastingAgencyTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'castingagency_test'
        # self.database_path = 'postgresql://postgres:' + password + '@localhost:5432/' + self.database_name
        self.database_path = "postgresql://postgres:{}@{}/{}".format(password, 'localhost:5432', self.database_name)
        'postgresql://postgres:' + password + '@localhost:5432/fyyur'
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()
    
    def tearDown(self):
        pass

    # GET /movies
        # pass
    # def test_get_movies(self):
    #     res = self.client().get('/movies', headers={'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjBPTnpYME9LaUt2MVpDTXNpYnd4VSJ9.eyJpc3MiOiJodHRwczovL2Rldi04YnpkZjAxeC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA5MTYwNWE5MjVkMmMwMDY5Y2U2MjA2IiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTYyMDE0MDI3MCwiZXhwIjoxNjIwMTQ3NDcwLCJhenAiOiJrY3FEUkphUU8xVnNySEFSOXp6V2lZYjR1cE1BRFVkSSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOltdfQ.HvhVV8NVm_e3PbqMHaJxTrWVtjNd4fRfOAbaV3tIZp85QrQJqVsBfglvrx5cYRSC6T1qkxWYhfbTAolQHeXjtDXF8Wf8aiyrhSr6iACimmP5nXfpj1clwywjk8joYv-PJOdg1fsGnQO2d7kJ7OPVdZqjAX7B7Nu4cciNJQPHg3xAhqIhl5Bkk0_np44Dn8jdOwxn-GBen7w_CznWyF56JwiGn9s8V7l0rJM0VLHLFau6F10URLfexIqqTASqS3N_cpnAlQ-XVjhF19Bp0H0Cg_fxLbQwotWPxFxRC_y02_vGdVUzKMrC1bVXdIV2yhPRhFFYC35YXtbDpwh545RZ9A'})
    #     print(res.data)
    #     if not res.data:
    #         print('Nothing here')
    #     data = json.loads(res.data)
    def test_get_movies(self):
        res = self.client().get('/movies')
        print(res.data)
        data = res.json()
        # fail
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