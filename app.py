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

@APP.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
  response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE')
  return response
'''
Endpoints 
'''
@APP.route('/movies', methods=['GET'])
def get_movies():
  try:
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
  except:
    abort(500, description="Internal Server Error")
  return jsonify(formattedMovies)

@APP.route('/movies', methods=['POST'])
def post_movie():
  request_data = request.get_json()
  if (request_data == None):
    abort(400, description="Empty Body Request")
  # check if there is request data and it contains the right data
  if ('title' in request_data and 'date' in request_data):
    title = request_data['title']
    try:
      date = datetime.datetime.strptime(request_data['date'], "%m/%d/%Y")
    except ValueError as e:
      abort(400, description=str(e))
    try:
      newMovie = Movie(title=title, release_date=date)
      db.session.add(newMovie)
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      abort(500, description=str(e))
  else:
    abort(400, description='request body did not include either or title and date')
  return 'done'

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

@APP.route('/actors', methods=['POST'])
def post_actor():
  try:
    request_data = request.get_json()
    # check if there is request data and it contains the right data
    if ((request_data['name']) and (request_data['age']) and (request_data['gender']) and (request_data['movie_id'])):
      name = request_data['name']
      age = request_data['age']
      gender = request_data['gender']
      movie_id = request_data['movie_id']
      newActor = Actor(name=name, age=age, gender=gender, movie_id=movie_id)
      db.session.add(newActor)
      db.session.commit()
    else:
      abort(400)
    return 'done'
  except:
    db.session.rollback()
    abort(400)

@APP.route('/actors/<int:actor_id>', methods=['PATCH'])
def patch_actor(actor_id):
  print(actor_id)
  # check if actor object exist in database
  actor = Actor.query.filter_by(id=actor_id).first()
  if actor == None:
    abort(404)
  else:
    request_data = request.get_json()
    # update name - if new name provided
    if ('name' in request_data):
      try:
        actor.name = request_data['name']
        db.session.commit()
      except:
        db.session.rollback()
        abort(400)
    # update age - if new age provided
    if ('age' in request_data):
      try:
        actor.age = request_data['age']
        db.session.commit()
      except:
        db.session.rollback()
        abort(400)
  return jsonify('updates complete')

@APP.route('/actors/<int:actor_id>', methods=['DELETE'])
def delete_actor(actor_id):
  print(actor_id)
  # check if actor object exist in database
  actor = Actor.query.filter_by(id=actor_id).first()
  if actor == None:
    abort(404)
  else:
    try:
      # delete actor object
      db.session.delete(actor)
      db.session.commit()
    except:
      db.session.rollback()
      abort(500)
  return jsonify({ "deleted actor with id": actor_id})

'''
Error Handler 
'''

@APP.errorhandler(400)
def bad_request(e):
  return jsonify(status_code=400, error=str(e.description)), 400

@APP.errorhandler(403)
def page_not_found(e):
  return jsonify(status_code=403, error="Forbidden"), 403

@APP.errorhandler(404)
def not_found(e):
  return jsonify(status_code=404, error="Not Found"), 404

@APP.errorhandler(410)
def page_not_found(e):
  return jsonify(status_code=410, error="Gone"), 410

@APP.errorhandler(500)
def page_not_found(e):
  return jsonify(status_code=500, error=str(e.description)), 500

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)