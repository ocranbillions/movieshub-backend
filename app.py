import os
from flask_cors import CORS
from flask import Flask, jsonify
from models import setup_db
from models import Movie, Actor


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
            'message': 'Be cool, man, be coooool! You\'re almost a FSND grad!!!',
            'moves': [movie.format() for movie in movies],
        }), 200

    return app


app = create_app()

if __name__ == '__main__':
    app.run()