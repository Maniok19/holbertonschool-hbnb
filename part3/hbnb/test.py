#!/usr/bin/env python3
"""Unit tests for the HBnB API."""

import unittest
import json
from run import app


class TestHBnBAPI(unittest.TestCase):
    """Test suite for the HBnB API endpoints."""

    def setUp(self):
        """Set up the test client."""
        self.app = app.test_client()
        self.app.testing = True
        self.user_id = self.create_user()
        self.token = self.login()

    def create_user(self):
        """Test creating a new user."""
        response = self.app.post('/api/v1/users/', json={
            "email": "mano@mano.mano",
            "password": "manomano",
            "first_name": "mano",
            "last_name": "mano"
        })
        self.assertEqual(response.status_code, 201)
        user_id = json.loads(response.data)['id']
        self.assertTrue(user_id)
        return user_id

    def login(self):
        """Test logging in."""
        response = self.app.post('/api/v1/auth/login', json={
            "email": "mano@mano.mano",
            "password": "manomano"
        })
        self.assertEqual(response.status_code, 200)
        token = json.loads(response.data)['access_token']
        self.assertTrue(token)
        return token
    
    def test_create_amenity(self):
        """Test creating a new amenity."""
        token = self.login()
        headers = {'Authorization': f'Bearer {token}'}
        
        response = self.app.post('/api/v1/amenities/', 
            json={
                'name': 'Swimming Pool'
            },
            headers=headers)
    
        self.assertEqual(response.status_code, 201)
        amenity_id = json.loads(response.data)['id']
        self.assertTrue(amenity_id)
    
    def test_create_place(self):
        """Test creating a new place."""
        # Get the token from the login method
        token = self.login()
        headers = {'Authorization': f'Bearer {token}'}
        
        response = self.app.post('/api/v1/places/', 
            json={
                'title': 'My Place',
                'description': 'A place to stay',
                'price': 100.00,  # Changed from float(100.00) to plain 100.00
                'latitude': 37.7749,  # Changed from float(37.7749)
                'longitude': -122.4194,  # Changed from float(-122.4194)
                'owner_id': self.user_id,
                'amenities': []
            },
            headers=headers)
        
        self.assertEqual(response.status_code, 201)
        place_id = json.loads(response.data)['id']
        self.assertTrue(place_id)

if __name__ == '__main__':
    unittest.main()