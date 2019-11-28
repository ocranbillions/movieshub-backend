import os
import unittest
import json

from app import create_app
from models import setup_db, Movie, Actor

casting_assistant = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ik1EWkdRVVUwTjBVNVFrUkNOVFpFTmpBeE1VTTBSVFJDTlVJME5EWXlNak00UVRsQ01qUkdRUSJ9.eyJpc3MiOiJodHRwczovL29jcmFuLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZGRlNjYxZThiNTliMTBlMTk4NTQ1MGMiLCJhdWQiOiJtb3ZpZXMiLCJpYXQiOjE1NzQ5MjU2ODIsImV4cCI6MTU3NDk5NzY4MSwiYXpwIjoiY2xpVm5pNDBKc2syZ1BtTWt3NDN2WGhZOGM2NVV5cWwiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.BboQR6TEBmAAdMdQ3ebKi-hYYb0w95tSdB8J7A0hwy2YrMswjbee3hXkvXCG0Vuj3A_uRb9-DBxb4PNzIYwozOc3jzYxpHXtjx-WacUTNLjT4FpsRaXdrg7W7Cgz0hrEnUbZ-u-LY_VsvtGXwwiC-0Ftma6mTEqXSvrkquHds-zsi4pS6IsGIN6v0MyeS8M5QiQ72Ex3ULLA_vXVWhShAIY3daclZHcvHKRDWILemDitdBaX-UW8I0jQdm1H-ZwLa4XCFL98tH1FhTu8Pd7yEE0m8aUHBRIy8o30CcZaToXRuNvPVjmp7wzPXwwH8XoEwzHwCO47onNaJNlSwyfa6A'
casting_director = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ik1EWkdRVVUwTjBVNVFrUkNOVFpFTmpBeE1VTTBSVFJDTlVJME5EWXlNak00UVRsQ01qUkdRUSJ9.eyJpc3MiOiJodHRwczovL29jcmFuLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZGRlNjUxYzc2OWEyZDBlZDNhZjUwNGYiLCJhdWQiOiJtb3ZpZXMiLCJpYXQiOjE1NzQ5MjU0NDEsImV4cCI6MTU3NDk5NzQ0MCwiYXpwIjoiY2xpVm5pNDBKc2syZ1BtTWt3NDN2WGhZOGM2NVV5cWwiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.JZlSEw9wKl6j1G-EydmB51EJaLtaoHk-O5oxeUf7IUzeEmANwgwnM9_tdLo672AM_WjllcZArVDQ1crja7t91DVor4z1DS9N73HC0XHvitgtl3Qa5P9HjqOqcNBMsWjZGQ4ibaTavc-P9bl3G5UsyeNOK89MW7PsK2vp-iH2lQG3CdP-vriXkpsqMDttdg_DQPjRT6qRNVSoEjzLzWItz98OHCw1LpIawOMNKU7jYy0IGY__15Eu_FSf-lzKTDZEmLYo4erWvaS6hz9om5ymLoj8gp2aVWM_DAA8JWQNZ5-zAHMNo1FwJw0ZcV4_i2y-w2066f1dduFWx1PGbuIIYw'
executive_producer = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ik1EWkdRVVUwTjBVNVFrUkNOVFpFTmpBeE1VTTBSVFJDTlVJME5EWXlNak00UVRsQ01qUkdRUSJ9.eyJpc3MiOiJodHRwczovL29jcmFuLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZGRlNjE0NmQ2NzBhZDBkMmIwMDVkODMiLCJhdWQiOiJtb3ZpZXMiLCJpYXQiOjE1NzQ5MjUyMjgsImV4cCI6MTU3NDk5NzIyNywiYXpwIjoiY2xpVm5pNDBKc2syZ1BtTWt3NDN2WGhZOGM2NVV5cWwiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.Zzn9daOYfrRs4dB81hIOReVUPOt1SC9cgR20PwYKO6jSkx8NId41uulfzZCL7R9zHSVXQZM-xbR9wXjPwa7VCZL_oVOwhFz7W5WTlo8vjkeRVx0dpPqyIFMrZaNORmU9epqFwBUAWrRdZWNAtGjbtMDK5aFViR0vXGKbafCioEmTd5Qi1N8c_z9xf3zn78jkrKvFsuazS3N8ji8QEso5SRNR33gxVM07F882KK2JFYg3pLZTSyo5yBrRfvZDIbvtEJxGW0Jfw08XvWt1miqz4FlTFKg7DSMRPPrlckMu0BvjYqtPCoA-wo0RgKhju1T2RNuOonx2MnakpvMIGxkUhw'

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
            headers={"Authorization": "Bearer " + casting_assistant}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
    
    # GET /movies/id
    def test_get_movie_by_id(self):
        response = self.client().get(
            '/movies/1',
            headers={"Authorization": "Bearer " + casting_assistant}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertEqual(data['movie']['title'], 'Black Panther')
    
    def test_get_movie_by_id_404(self):
        response = self.client().get(
            '/movies/10000',
            headers={"Authorization": "Bearer " + casting_assistant}
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
            headers={"Authorization": "Bearer " + executive_producer}
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
            headers={"Authorization": "Bearer " + executive_producer}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request, pls check your inputs')
    
    def test_post_movie_401(self):
        response = self.client().post(
            '/movies',
            json={'title': 'Wrong movie', 'release_date': "1984-01-23"},
            headers={"Authorization": "Bearer " + casting_assistant}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message']['code'], 'unauthorized')
    
    # PATCH /movies
    def test_edit_movie(self):
        response = self.client().patch(
            '/movies/2',
            json={'title': 'The Hangover', 'release_date': "2018-10-12"},
            headers={"Authorization": "Bearer " + casting_director}
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
            headers={"Authorization": "Bearer " + casting_director}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request, pls check your inputs')

    def test_edit_movie_404(self):
        response = self.client().patch(
            '/movies/50000',
            json={'title': 'Black Panther 2', 'release_date': "2019-11-12"},
            headers={"Authorization": "Bearer " + casting_director}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')
    
    # DELETE /movies/id
    def test_delete_movie(self):
        response = self.client().delete(
            '/movies/3',
            headers={
                "Authorization": "Bearer " + executive_producer
            }
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Movie deleted')

    def test_delete_movie_404(self):
        response = self.client().delete(
            '/movies/110000',
            headers={"Authorization": "Bearer " + executive_producer}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')
    
    def test_delete_movie_401(self):
        response = self.client().delete(
            '/movies/1',
            headers={"Authorization": "Bearer " + casting_assistant}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message']['code'], 'unauthorized')
    

    # ==========================================================================================================
    #  GET /actors
    def test_get_actors(self):
        response = self.client().get(
            '/actors',
            headers={"Authorization": "Bearer " + casting_assistant}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
    
    # GET /actors/id
    def test_get_actor_by_id(self):
        response = self.client().get(
            '/actors/1',
            headers={"Authorization": "Bearer " + casting_assistant}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
        self.assertEqual(data['actor']['name'], 'Pierce Brosnan')
    
    def test_get_actor_by_id_404(self):
        response = self.client().get(
            '/actors/10000',
            headers={"Authorization": "Bearer " + casting_assistant}
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
            headers={"Authorization": "Bearer " + casting_director}
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
            headers={"Authorization": "Bearer " + casting_director}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request, pls check your inputs')
    
    def test_post_actor_401(self):
        response = self.client().post(
            '/actors',
            json={'name': 'Jude', 'age': 44, "gender": "male"},
            headers={"Authorization": "Bearer " + casting_assistant}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message']['code'], 'unauthorized')
    
    # PATCH /actors
    def test_edit_actor(self):
        response = self.client().patch(
            '/actors/2',
            json={'name': 'Cynthia', 'age': 27, "gender": "female"},
            headers={"Authorization": "Bearer " + casting_director}
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
            headers={"Authorization": "Bearer " + casting_director}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request, pls check your inputs')

    def test_edit_actor_404(self):
        response = self.client().patch(
            '/actors/50000',
            json={'name': 'Cynthia', 'age': 27, "gender": "female"},
            headers={"Authorization": "Bearer " + casting_director}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')
    
    # DELETE /actors/id
    def test_delete_actor(self):
        response = self.client().delete(
            '/actors/3',
            headers={"Authorization": "Bearer " + casting_director}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Actor deleted')

    def test_delete_actor_404(self):
        response = self.client().delete(
            '/actors/110000',
            headers={"Authorization": "Bearer " + casting_director}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')
    
    def test_delete_actor_401(self):
        response = self.client().delete(
            '/actors/1',
            headers={"Authorization": "Bearer " + casting_assistant}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message']['code'], 'unauthorized')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()