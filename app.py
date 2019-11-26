import os
from flask_cors import CORS
from flask import Flask, jsonify, abort
from models import setup_db, db, Movie, Actor


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def get_greeting():
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



    '''
    Create error handlers for all expected errors
    '''
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