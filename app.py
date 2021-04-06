import os, sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor, db
from sqlalchemy.exc import IntegrityError
import datetime

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)
  setup_db(app)

  return app

APP = create_app()

'''
Endpoints 
'''
@APP.route('/movies', methods=['GET'])
def get_movies():
  movies = Movie.query.all()
  formattedMovies = []
  for movie in movies:
        formattedActors = []
        for actor in movie.actors:
              formattedActors.append({
                "id": actor.id,
                "name": actor.name,
                "age": actor.age,
                "gender": actor.gender,
              })
        formattedMovies.append({
          "id": movie.id, 
          "title": movie.title, 
          "release_date": movie.release_date.strftime('%m/%d/%Y'),
          "actors": formattedActors
        })
  return jsonify(formattedMovies)

@APP.route('/movies', methods=['POST'])
def post_movie():
  try:
    request_data = request.get_json()
    # check if there is request data and it contains the right data
    if ((request_data['title']) and (request_data['date'])):
      title = request_data['title']
      date = datetime.datetime.strptime(request_data['date'], "%m/%d/%Y")
      newMovie = Movie(title=title, release_date=date)
      db.session.add(newMovie)
      db.session.commit()
      print(newMovie)
    else:
      db.session.rollback()
      abort(400)
    return 'done'
  except:
    abort(400)

@APP.route('/actors', methods=['GET'])
def get_actors():
  actors = Actor.query.all()
  formattedActors = []
  for actor in actors:
    formattedActors.append({
      "id": actor.id,
      "name": actor.name,
      "age": actor.age,
      "gender": actor.gender
    })
  return jsonify(formattedActors)

'''
Error Handler 
'''

@APP.errorhandler(400)
def bad_request(e):
  return jsonify(status_code=400, error="Bad Request"), 400

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