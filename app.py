import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)

  return app

APP = create_app()
setup_db(APP)

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)