import unittest
import uuid
from app import create_app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.user_email = f"test{uuid.uuid4()}@example.com"
        self.user_password = "password123"
        self.user_id = self.create_test_user()
        self.token = self.create_token()
        self.place_id = self.create_place()

    def create_test_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Test",
            "last_name": "User",
            "email": self.user_email,
            "password": self.user_password
        })
        self.assertEqual(response.status_code, 201, f"Error creating user: {response.json}")
        user_id = response.json.get("id")
        return user_id
    
    def create_token(self):
        response = self.client.post('/api/v1/auth/login', json={
            "email": self.user_email,
            "password": self.user_password
        })
        self.assertEqual(response.status_code, 200, f"Error logging in: {response.json}")
        token = response.json.get("access_token")
        return token

    def create_place(self):
        place_title = f"Test{uuid.uuid4()}"
        response = self.client.post('/api/v1/places/', json={
            "title": place_title,
            "description": "A test place description",
            "price": 100.0,
            "latitude": 45.0,
            "longitude": -75.0,
            "owner_id": self.user_id,
            "amenities": []
        }, headers={"Authorization": f"Bearer {self.token}"})
        self.assertEqual(response.status_code, 201, f"Error creating place: {response.json}")
        place_id = response.json.get("id")
        return place_id
    
    def test_create_review(self):
        response = self.client.post('/api/v1/reviews/', json={
            "user_id": self.user_id,
            "place_id": self.place_id,
            "text": "Great place to stay!",
            "rating": 5  # Ajout du champ 'rating'
        }, headers={"Authorization": f"Bearer {self.token}"})
        self.assertEqual(response.status_code, 201, f"Error creating review: {response.json}")

    # NORMAL POST REQUEST

    def test_create_user_login_create_place(self):
        # Create a place using the token
        response = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "description": "A test place description",
            "price": 100.0,
            "latitude": 45.0,
            "longitude": -75.0,
            "owner_id": self.user_id,
            "amenities": []
        }, headers={"Authorization": f"Bearer {self.token}"})
        self.assertEqual(response.status_code, 201, f"Error creating place: {response.json}")

    def test_create_user_login_create_place_wrong_owner(self):
        # Create a place using the token, but with a different owner_id
        # CREATE wrong owner
        response1 = self.client.post('/api/v1/users/', json={
            "first_name": "Test",
            "last_name": "User2",
            "email": f"test{uuid.uuid4()}@example.com",
            "password": "password123"
        })
        self.assertEqual(response1.status_code, 201, f"Error creating user: {response1.json}")
        user_id = response1.json.get("id")
        response = self.client.post('/api/v1/places/', json={
            "title": "Test Place2",
            "description": "A test place description",
            "price": 100.0,
            "latitude": 45.0,
            "longitude": -75.0,
            "owner_id": user_id,
            "amenities": []
        }, headers={"Authorization": f"Bearer {self.token}"})
        self.assertEqual(response.status_code, 403, f"Error creating place: {response.json}")

    def test_create_user_login_create_place_no_token(self):
        # Create a place without a token
        response = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "description": "A test place description",
            "price": 100.0,
            "latitude": 45.0,
            "longitude": -75.0,
            "owner_id": self.user_id,
            "amenities": []
        })
        self.assertEqual(response.status_code, 401, f"Error creating place: {response.json}")

    def test_update_place(self):
        # update a place using the token
        place_title = f"Test{uuid.uuid4()}"
        response = self.client.put(f'/api/v1/places/{self.place_id}', json={
            "title": place_title,
            "description": "A test place description",
            "price": 100.0,
            "latitude": 45.0,
            "longitude": -75.0,
            "owner_id": self.user_id,
            "amenities": []
        }, headers={"Authorization": f"Bearer {self.token}"})
        self.assertEqual(response.status_code, 200, f"Error updating place: {response.json}")
    
    def test_update_place_no_token(self):
        # update a place without a token
        place_title = f"Test{uuid.uuid4()}"
        response = self.client.put(f'/api/v1/places/{self.place_id}', json={
            "title": place_title,
            "description": "A test place description",
            "price": 100.0,
            "latitude": 45.0,
            "longitude": -75.0,
            "owner_id": self.user_id,
            "amenities": []
        })
        self.assertEqual(response.status_code, 401, f"Error updating place: {response.json}")
    
    def test_update_place_wrong_owner(self):
        # update a place with a wrong owner
        response1 = self.client.post('/api/v1/users/', json={
            "first_name": "Test",
            "last_name": "User2",
            "email": f"test{uuid.uuid4()}@example.com",
            "password": "password123"
        })
        self.assertEqual(response1.status_code, 201, f"Error creating user: {response1.json}")
        user_id = response1.json.get("id")
        response = self.client.put(f'/api/v1/places/{self.place_id}', json={
            "title": "Test Place2",
            "description": "A test place description",
            "price": 100.0,
            "latitude": 45.0,
            "longitude": -75.0,
            "owner_id": user_id,
            "amenities": []
        }, headers={"Authorization": f"Bearer {self.token}"})
        self.assertEqual(response.status_code, 403, f"Error updating place: {response.json}")



if __name__ == '__main__':
    unittest.main()