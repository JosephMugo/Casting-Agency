import os
import unittest
import json

from app import create_app
from models import setup_db, Movie, Actor

class CastingAgencyTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = ''
        setup_db(self.app, self.database_path)
    
    def tearDown(self):
        pass

    # 

if __name__ == "__main__":
    unittest.main()