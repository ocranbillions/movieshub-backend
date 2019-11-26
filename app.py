import os
from flask_cors import CORS
from flask import Flask, jsonify, abort, request
from models import setup_db, db, Movie, Actor
from utils import *


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def welcome():
        return 'Welcome to Movies Hub!'


    @app.route('/movies')
    def get_movies():
        movies = Movie.query.all()
        return jsonify({
            'success': True,
            'movies': [movie.format() for movie in movies],
        }), 200
        
        
    @app.route('/movies/<int:id>')
    def get_movie_by_id(id):
        movie = Movie.query.get(id)

        if movie is None:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'movie': movie.format(),
            }), 200
    

    @app.route('/movies', methods=['POST'])
    def post_movie():
        data = request.get_json()
        title = data.get('title', '')
        date = data.get('release_date', '')
        
        movie = Movie(title=title, release_date=date)
        if validate_movie(movie) is False:
            abort(400)
        try:
            movie.insert()
            return jsonify({
                'success': True,
                'message': 'Movie added',
                'movie': movie.format()
            }), 201
        except:
            abort(500)
    

    @app.route('/movies/<int:id>', methods=['PATCH'])
    def edit_movie(id):
        data = request.get_json()
        title = data.get('title', '')
        date = data.get('release_date', '')

        movie = Movie.query.get(id)

        if movie is None:
            abort(404)

        movie.title = title
        movie.release_date = date
        if validate_movie(movie) is False:
            db.session.rollback()
            abort(400)
        try:
            movie.update()
            return jsonify({
                'success': True,
                'message': 'Movie updated',
                'movie': movie.format()
            }), 200
        except:
            db.session.rollback()
            abort(500)

    
    @app.route('/movies/<int:id>', methods=['DELETE'])
    def delete_movie(id):
        movie = Movie.query.get(id)

        if movie is None:
            abort(404)
        try:
            movie.delete()
            return jsonify({
                'success': True,
                'message': 'Movie deleted',
                'movie': movie.id
            })
        except:
            db.session.rollback()
            abort(500)
    

    '''
    ACTORS ENDPOINTS   
    '''
    @app.route('/actors')
    def get_actors():
        actors = Actor.query.all()
        return jsonify({
            'success': True,
            'actors': [actor.format() for actor in actors],
        }), 200
        
        
    @app.route('/actors/<int:id>')
    def get_actor_by_id(id):
        actor = Actor.query.get(id)

        if actor is None:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'actor': actor.format(),
            }), 200


    @app.route('/actors', methods=['POST'])
    def post_actor():
        data = request.get_json()
        name = data.get('name', '')
        age = data.get('age', '')
        gender = data.get('gender', '')
        
        actor = Actor(name=name, age=age, gender=gender)
        if validate_actor(actor) is False:
            abort(400)
        try:
            actor.insert()
            return jsonify({
                'success': True,
                'message': 'Actor added',
                'actor': actor.format()
            }), 201
        except:
            abort(500)


    @app.route('/actors/<int:id>', methods=['PATCH'])
    def edit_actor(id):
        data = request.get_json()
        name = data.get('name', '')
        age = data.get('age', '')
        gender = data.get('gender', '')

        actor = Actor.query.get(id)

        if actor is None:
            abort(404)

        actor.name = name
        actor.age = age
        actor.gender = gender
        if validate_actor(actor) is False:
            db.session.rollback()
            abort(400)
        try:
            actor.update()
            return jsonify({
                'success': True,
                'message': 'Actor updated',
                'actor': actor.format()
            }), 200
        except:
            db.session.rollback()
            abort(500)
    
    @app.route('/actors/<int:id>', methods=['DELETE'])
    def delete_actor(id):
        actor = Actor.query.get(id)

        if actor is None:
            abort(404)
        try:
            actor.delete()
            return jsonify({
                'success': True,
                'message': 'Actor deleted',
                'actor': actor.id
            })
        except:
            db.session.rollback()
            abort(500)

    '''
    Create error handlers for all expected errors
    '''
    # handle bad request
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "message": "Bad Request, pls check your inputs"
        }), 400

    # handle resource not found errors
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "message": "Resource not found"
        }), 404

    # handle bad request
    @app.errorhandler(500)
    def bad_request(error):
        return jsonify({
            "success": False,
            "message": "Something went wrong, please try again"
        }), 500


    return app


app = create_app()

if __name__ == '__main__':
    app.run()