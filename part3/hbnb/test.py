#!/usr/bin/env python3
"""Unit tests for the HBnB API."""

import unittest
import json
import uuid
from run import app
from flask_jwt_extended import create_access_token


class TestHBnBAPI(unittest.TestCase):
    """Test suite for the HBnB API endpoints."""

    def setUp(self):
        """Set up the test client."""
        self.app = app.test_client()
        self.app.testing = True
        
        # Generate a unique email for each test run
        unique_id = str(uuid.uuid4())[:8]
        self.test_email = f"test_{unique_id}@example.com"
        self.test_password = "password123"
        
        # Create user and get ID
        self.user_id = self.create_user()
        # Get authentication token
        self.token = self.login()

    def create_user(self):
        """Create a new user with unique email."""
        response = self.app.post('/api/v1/users/', json={
            "email": self.test_email,
            "password": self.test_password,
            "first_name": "Test",
            "last_name": "User"
        })
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        self.assertTrue('id' in response_data)
        return response_data['id']

    def login(self):
        """Test logging in."""
        response = self.app.post('/api/v1/auth/login', json={
            "email": self.test_email,
            "password": self.test_password
        })
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertTrue('access_token' in response_data)
        return response_data['access_token']
    
    def test_create_amenity(self):
        """Test creating a new amenity."""
        # Generate a unique amenity name
        unique_name = f"Swimming Pool {uuid.uuid4()}"
        
        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.app.post('/api/v1/amenities/', 
            json={
                'name': unique_name
            },
            headers=headers)
        
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        self.assertTrue('id' in response_data)
    
    def test_create_place(self):
        """Test creating a new place."""
        # Generate a unique place title
        unique_title = f"My Place {uuid.uuid4()}"
        
        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.app.post('/api/v1/places/', 
            json={
                'title': unique_title,
                'description': 'A place to stay',
                'price': 100.00,
                'latitude': 37.7749,
                'longitude': -122.4194,
                'owner_id': self.user_id,
                'amenities': []
            },
            headers=headers)
        
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        self.assertTrue('id' in response_data)


if __name__ == '__main__':
    unittest.main()