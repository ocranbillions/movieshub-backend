import os
import unittest
import json

from app import create_app
from models import setup_db, Movie, Actor

EXECUTIVE_PRODUCER = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ik1EWkdRVVUwTjBVNVFrUkNOVFpFTmpBeE1VTTBSVFJDTlVJME5EWXlNak00UVRsQ01qUkdRUSJ9.eyJpc3MiOiJodHRwczovL29jcmFuLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZGRlNjE0NmQ2NzBhZDBkMmIwMDVkODMiLCJhdWQiOiJtb3ZpZXMiLCJpYXQiOjE1NzUxMzY5OTUsImV4cCI6MTU3NTIwODk5NCwiYXpwIjoiY2xpVm5pNDBKc2syZ1BtTWt3NDN2WGhZOGM2NVV5cWwiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.rQjzRjWMoBVxkI4wdrj8icNFn0Q9u8fEk2ayrq32eJCnFOw0bLtJHqV9M1UVIdC49PtkLLHVZj3Oad8NR9sK-PadOWIGqppUN7oLEukQprxp0tZjdlkZmPmB5T9ZSC-W8fdkMhVzxAUZtI04Z9JEOsBd6e4FPI9spu_Bf9rYCruC-RObqlh0_N6F5gVKteJYJxOhsnE0l83uhFdloAtPOFom02n-Iapn8qzn0ncnMWAadEwFZkqqnA4RIEJGWZy54pVlZRuLWuLIXGGu35Oe8OWbkJOrybyqw9kAqtgJuoh-IEITSQi3E9U7i0Ott7jy6dvnp1e4cp2pzywxmC7txQ'
CASTING_DIRECTOR = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ik1EWkdRVVUwTjBVNVFrUkNOVFpFTmpBeE1VTTBSVFJDTlVJME5EWXlNak00UVRsQ01qUkdRUSJ9.eyJpc3MiOiJodHRwczovL29jcmFuLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZGRlNjUxYzc2OWEyZDBlZDNhZjUwNGYiLCJhdWQiOiJtb3ZpZXMiLCJpYXQiOjE1NzUxMzY4ODAsImV4cCI6MTU3NTIwODg3OSwiYXpwIjoiY2xpVm5pNDBKc2syZ1BtTWt3NDN2WGhZOGM2NVV5cWwiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.SxcKJ8hnfmusn9EFimcbqZ9xFDoDp_u7MfzjO68rkcLDClV7Wydyrw79UJbIKi1pEARTGGzOF3MQXy9a8sVLaN_KmXwdV3fiJyBdpA8Rf9HKb7v7i6_5V_DQBIaTmUXOruQ0utaJ-LHek-KFFScHYBUnUnsL1ubVqLgEx3i7_c5vzeL8OyoXtu0BlX8azHwLTg0cZhIBUAsT7omXCYT-XaNwGJdoL8gtef-HnaJYk_sIp23W3-vqBwGHX2fpetBeqncfFiHqySmezAUKUbGXGNmY0VIy6whxZR3jxNKMWYs4xd0he-iR9w-K-u0Rov_QFrY5xOjIGlpCEA__CELtnA'
CASTING_ASSISTANT = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ik1EWkdRVVUwTjBVNVFrUkNOVFpFTmpBeE1VTTBSVFJDTlVJME5EWXlNak00UVRsQ01qUkdRUSJ9.eyJpc3MiOiJodHRwczovL29jcmFuLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZGRlNjYxZThiNTliMTBlMTk4NTQ1MGMiLCJhdWQiOiJtb3ZpZXMiLCJpYXQiOjE1NzUxMzcwODQsImV4cCI6MTU3NTIwOTA4MywiYXpwIjoiY2xpVm5pNDBKc2syZ1BtTWt3NDN2WGhZOGM2NVV5cWwiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.jyXo1hKqFjCo7CUyZKDVNNGdXPJIq29_esY8gXAqHfAwlnXXiyfUfimXiKCwFRJsJgtyATBpydcN11_LSKYsvoItah2tc4UNDYhLChWCNI0YSu8iSFFiPVBZfLWuYAiJpuJ4F7Sn5Tav7cEA-X7pYrMpPIGj5YadHxF704QTkJwfkXbdSBQzCuDMyYE98vpD6Fq9cFJ-Pj8saceYe6Sc5sZVv6ahI4ahsqp6JdV4R8CQo3AljKEROnyiQ6EtOGNkBmzrZYiwWODXEjyDJzoa_fgRzZkRuQIws2__oULKtiSRfHScT2hwen_mXL738mvw3LkFrcR52rm_alCI_Clw9Q'


class MHTestCase(unittest.TestCase):
    """This class represents the movies-hub test case"""
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['TEST_DATABASE_URL']

        setup_db(self.app, self.database_path)

    def tearDown(self):
        """Executed after reach test"""
        pass

    #  GET /movies
    def test_get_movies(self):
        response = self.client().get(
            '/movies',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    # GET /movies/id
    def test_get_movie_by_id(self):
        response = self.client().get(
            '/movies/1',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertEqual(data['movie']['title'], 'Black Panther')

    def test_get_movie_by_id_404(self):
        response = self.client().get(
            '/movies/10000',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertEqual(data['message'], 'Resource not found')

    # POST /movies
    def test_post_movie(self):
        response = self.client().post(
            '/movies',
            json={'title': 'Jumanji', 'release_date': "1981-02-19"},
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Movie added')
        self.assertEqual(data['movie']['title'], 'Jumanji')

    def test_post_movie_400(self):
        response = self.client().post(
            '/movies',
            json={'title': '', 'release_date': ""},
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request, pls check your inputs')

    def test_post_movie_401(self):
        response = self.client().post(
            '/movies',
            json={'title': 'Wrong movie', 'release_date': "1984-01-23"},
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message']['code'], 'unauthorized')

    # PATCH /movies
    def test_edit_movie(self):
        response = self.client().patch(
            '/movies/2',
            json={'title': 'The Hangover', 'release_date': "2018-10-12"},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Movie updated')
        self.assertEqual(data['movie']['title'], 'The Hangover')

    def test_edit_movie_400(self):
        response = self.client().patch(
            '/movies/1',
            json={'title': '', 'release_date': ""},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request, pls check your inputs')

    def test_edit_movie_404(self):
        response = self.client().patch(
            '/movies/50000',
            json={'title': 'Black Panther 2', 'release_date': "2019-11-12"},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    # DELETE /movies/id
    def test_delete_movie(self):
        response = self.client().delete(
            '/movies/3',
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Movie deleted')

    def test_delete_movie_404(self):
        response = self.client().delete(
            '/movies/110000',
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_delete_movie_401(self):
        response = self.client().delete(
            '/movies/1',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message']['code'], 'unauthorized')


    # ==========================================================================================================
    #  GET /actors
    def test_get_actors(self):
        response = self.client().get(
            '/actors',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    # GET /actors/id
    def test_get_actor_by_id(self):
        response = self.client().get(
            '/actors/1',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
        self.assertEqual(data['actor']['name'], 'Pierce Brosnan')

    def test_get_actor_by_id_404(self):
        response = self.client().get(
            '/actors/10000',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertEqual(data['message'], 'Resource not found')

    # POST /actors
    def test_post_actor(self):
        response = self.client().post(
            '/actors',
            json={'name': 'David', 'age': 44, "gender": "male"},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Actor added')
        self.assertEqual(data['actor']['name'], 'David')

    def test_post_actor_400(self):
        response = self.client().post(
            '/actors',
            json={'name': '', 'age': '', "gender": ""},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request, pls check your inputs')

    def test_post_actor_401(self):
        response = self.client().post(
            '/actors',
            json={'name': 'Jude', 'age': 44, "gender": "male"},
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message']['code'], 'unauthorized')

    # PATCH /actors
    def test_edit_actor(self):
        response = self.client().patch(
            '/actors/2',
            json={'name': 'Cynthia', 'age': 27, "gender": "female"},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Actor updated')
        self.assertEqual(data['actor']['name'], 'Cynthia')

    def test_edit_actor_400(self):
        response = self.client().patch(
            '/actors/2',
            json={'name': '', 'age': '', "gender": ""},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request, pls check your inputs')

    def test_edit_actor_404(self):
        response = self.client().patch(
            '/actors/50000',
            json={'name': 'Cynthia', 'age': 27, "gender": "female"},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    # DELETE /actors/id
    def test_delete_actor(self):
        response = self.client().delete(
            '/actors/3',
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Actor deleted')

    def test_delete_actor_404(self):
        response = self.client().delete(
            '/actors/110000',
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_delete_actor_401(self):
        response = self.client().delete(
            '/actors/1',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message']['code'], 'unauthorized')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
