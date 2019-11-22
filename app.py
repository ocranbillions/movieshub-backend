import os
from flask_cors import CORS
from flask import Flask, jsonify
from config import setup_db
from manage import Person

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def get_greeting():
        excited = os.environ['EXCITED']
        greeting = "Hello" 
        if excited == 'true': greeting = greeting + "!!!!!"
        return greeting

    @app.route('/coolkids')
    def be_cool():
        people = Person.query.all()
        return jsonify({
            'message': 'Be cool, man, be coooool! You\'re almost a FSND grad!',
            'people': [person.format() for person in people],
        }), 200

    return app

app = create_app()

if __name__ == '__main__':
    app.run()