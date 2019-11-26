import os
import unittest
import json
# from flask_sqlalchemy import SQLAlchemy

from app import create_app
# from app import app
from models import setup_db, Movie, Actor

class MHTestCase(unittest.TestCase):
    """This class represents the movies-hub test case"""
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        # self.app = app
        self.client = self.app.test_client
        self.database_path = os.environ['TEST_DATABASE_URL']

        setup_db(self.app, self.database_path)

        # binds the app to the current context
        # with self.app.app_context():
        #     self.db = SQLAlchemy()
        #     self.db.init_app(self.app)
        #     # create all tables
        #     self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    #  GET /movies
    def test_get_movies(self):
        response = self.client().get('/movies')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        # self.assertEqual(len(data['movies']), 1)
    
    # GET /movies/id
    def test_get_movie_by_id(self):
        response = self.client().get('/movies/1')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertEqual(data['movie']['title'], 'Black Panther')
    
    def test_get_movie_by_id_404(self):
        response = self.client().get('/movies/10000')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertEqual(data['message'], 'Resource not found')

    # POST /movies 
    def test_post_movie(self):
        payload = {
            'title': 'Jumanji',
            'release_year': 1981,
        }
        response = self.client().post('/movies', json=payload)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Movie added')
        self.assertEqual(data['movie']['title'], 'Jumanji')

    def test_post_movie_400(self):
        payload = {
            'title': '',
            'release_year': '',
        }
        response = self.client().post('/movies', json=payload)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request, pls check your inputs')

    
    # PATCH /movies
    def test_edit_movie(self):
        payload = {
            'title': 'Black Panther',
            'release_year': 2018,
        }
        response = self.client().patch('/movies/1', json=payload)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Movie updated')
        self.assertEqual(data['movie']['title'], 'Black Panther')

    def test_edit_movie_400(self):
        payload = {
            'title': '',
            'release_year': '',
        }
        response = self.client().patch('/movies/1', json=payload)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request, pls check your inputs')

    def test_edit_movie_404(self):
        payload = {
            'title': 'Black Panther',
            'release_year': 2018,
        }
        response = self.client().patch('/movies/500000', json=payload)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')
    
    # DELETE /movies/id
    def test_delete_movie(self):
        response = self.client().delete('/movies/12')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Movie deleted')

    def test_delete_movie_404(self):
        response = self.client().delete('/movies/110000')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')


# dropdb trivia_test && createdb trivia_test
# psql trivia_test < trivia.psql && python test_flaskr.py

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()