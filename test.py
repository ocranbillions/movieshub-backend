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

    def test_get_movies(self):
        response = self.client().get('/movies')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertEqual(len(data['movies']), 1)
    
    def test_get_movie_by_id(self):
        response = self.client().get('/movies/1')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertEqual(data['movie']['title'], 'Avengers')
    
    def test_get_movie_by_id_404(self):
        response = self.client().get('/movies/10000')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertEqual(data['message'], 'Resource not found')

    # def test_get_questions(self):
    #     response = self.client().get('/questions')
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue(data['total_questions'])
    #     self.assertTrue(data['categories'])
    #     self.assertTrue(data['questions'])

    # def test_successful_delete(self):
    #     res = self.client().delete('/questions/11')
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['message'], 'Successfully deleted')

    # def test_unsuccessful_delete(self):
    #     res = self.client().delete('/questions/10000')
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'Unprocessable Entity')

    # def test_create_question(self):
    #     payload = {
    #         'question': 'The answer to life, the universe and everything?',
    #         'answer': 42,
    #         'difficulty': 3,
    #         'category': 1,
    #     }
    #     response = self.client().post('/questions', json=payload)
    #     data = json.loads(response.data)
    #     self.assertEqual(response.status_code, 201)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['message'], 'Successfully Created!')

    # def test_400_create_question(self):
    #     payload = {
    #         'question': '',
    #         'answer': '',
    #         'difficulty': 3,
    #         'category': 1,
    #     }
    #     response = self.client().post('/questions', json=payload)
    #     data = json.loads(response.data)
    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'Bad Request, pls check your inputs')

    # def test_search_questions(self):
    #     payload = {
    #         'searchTerm': 'the human body',
    #     }
    #     response = self.client().post('/questions/search', json=payload)
    #     data = json.loads(response.data)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(len(data['questions']), 1)

    # def test_400_search_questions(self):
    #     payload = {
    #         'searchTerm': '',
    #     }
    #     response = self.client().post('/questions/search', json=payload)
    #     data = json.loads(response.data)
    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'Bad Request, pls check your inputs')

    # def test_404_search_questions(self):
    #     payload = {
    #         'searchTerm': 'somerandomsearchstring',
    #     }
    #     response = self.client().post('/questions/search', json=payload)
    #     data = json.loads(response.data)
    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'Resource not found')

    # def test_game_play(self):
    #     payload = {
    #         'previous_questions': [3],
    #         'quiz_category': {
    #             'type': 'Sports',
    #             'id': 6
    #         }
    #     }
    #     response = self.client().post('/quizzes', json=payload)
    #     data = json.loads(response.data)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['question'])

# dropdb trivia_test && createdb trivia_test
# psql trivia_test < trivia.psql && python test_flaskr.py

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()