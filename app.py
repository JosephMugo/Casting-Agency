import os, sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor, db
from sqlalchemy.exc import IntegrityError
import datetime
from auth import AuthError, requires_auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  print('runs')

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE')
    return response
  '''
  Endpoints 
  '''
  @app.route('/', methods=['GET'])
  def get_simple():
    return jsonify({"works": True})

  @app.route('/movies', methods=['GET'])
  @requires_auth('get:movies')
  def get_movies(jwt):
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
    return jsonify({"movies": formattedMovies})

  @app.route('/movies', methods=['POST'])
  @requires_auth('add:movies')
  def post_movie(jwt):
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

  @app.route('/actors', methods=['GET'])
  @requires_auth('get:actors')
  def get_actors(jwt):
    actors = Actor.query.all()
    formattedActors = []
    for actor in actors:
      formattedActors.append({
        "id": actor.id,
        "name": actor.name,
        "age": actor.age,
        "gender": actor.gender
      })
    return jsonify({"actors": formattedActors})

  @app.route('/actors', methods=['POST'])
  @requires_auth('add:actors')
  def post_actor(jwt):
    request_data = request.get_json()
    if (request_data == None):
      abort(400, description='Empty Body Request')
    # check if there is request data and it contains the right data
    if ('name' in request_data and 'age' in request_data and 'gender' in request_data and 'movie_id' in request_data):
      name = request_data['name']
      age = request_data['age']
      gender = request_data['gender']
      movie_id = request_data['movie_id']
      try:
        newActor = Actor(name=name, age=age, gender=gender, movie_id=movie_id)
        db.session.add(newActor)
        db.session.commit()
      except Exception as e:
        db.session.rollback()
        abort(500, description=str(e))
    else:
      abort(400, description='Missing required properties or property')
    return 'done'

  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  @requires_auth('update:actors')
  def patch_actor(jwt, actor_id):
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

  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(jwt, actor_id):
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

  @app.errorhandler(400)
  def bad_request(e):
    return jsonify(status_code=400, error=str(e.description)), 400

  @app.errorhandler(403)
  def page_not_found(e):
    return jsonify(status_code=403, error="Forbidden"), 403

  @app.errorhandler(404)
  def not_found(e):
    return jsonify(status_code=404, error="Not Found"), 404

  @app.errorhandler(410)
  def page_not_found(e):
    return jsonify(status_code=410, error="Gone"), 410

  @app.errorhandler(500)
  def page_not_found(e):
    return jsonify(status_code=500, error=str(e.description)), 500

  @app.errorhandler(AuthError)
  def handle_auth_error(ex):
      response = jsonify(ex.error)
      response.status_code = ex.status_code
      return response

  return app