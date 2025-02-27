#!/usr/bin/python3
import unittest
from app import create_app

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_user(self):
        """Test user creation with valid data"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_user_invalid_data(self):
        """Test user creation with invalid data"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)

    def test_get_users(self):
        """Test retrieving all users"""
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)

class TestPlaceEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_place(self):
        """Test creating a place with valid data"""
        response = self.client.post('/api/v1/places/', json={
            "title": "Beach House",
            "description": "Beautiful house near the beach",
            "price": 150.0,
            "latitude": 34.0522,
            "longitude": -118.2437,
            "owner_id": "12345",
            "amenities": ["WiFi", "Pool"]
        })
        self.assertEqual(response.status_code, 201)

    def test_get_places(self):
        """Test retrieving all places"""
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)

class TestReviewEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_review(self):
        """Test creating a review with valid data"""
        response = self.client.post('/api/v1/reviews/', json={
            "user_id": "123",
            "place_id": "456",
            "text": "Great place to stay!"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_review_invalid_data(self):
        """Test creating a review with missing data"""
        response = self.client.post('/api/v1/reviews/', json={
            "user_id": "",
            "place_id": "456",
            "text": ""
        })
        self.assertEqual(response.status_code, 400)

    def test_get_reviews(self):
        """Test retrieving all reviews"""
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()