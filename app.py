import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)
  setup_db(app)

  return app

APP = create_app()

'''
Error Handler 
'''

@APP.errorhandler(404)
def page_not_found(e):
  return jsonify(status_code=400, error="Not Found"), 400

@APP.errorhandler(403)
def page_not_found(e):
  return jsonify(status_code=403, error="Forbidden"), 403

@APP.errorhandler(410)
def page_not_found(e):
  return jsonify(status_code=410, error="Gone"), 410

@APP.errorhandler(500)
def page_not_found(e):
  return jsonify(status_code=500, error="Internal Server Error"), 500

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)