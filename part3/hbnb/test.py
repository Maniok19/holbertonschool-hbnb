#!/usr/bin/env python3
"""Unit tests for the HBnB API."""

import unittest
import json
import uuid
from run import app
from flask_jwt_extended import create_access_token
from app.models.user import User
from app import db, create_app


class TestHBnBAPI(unittest.TestCase):
    """Test suite for the HBnB API endpoints."""

    @classmethod
    def setUpClass(cls):
        """Set up test environment once before all tests."""
        cls.app = app.test_client()
        cls.app_context = app.app_context()
        cls.app_context.push()
        
        # Create an admin user for tests (directly in database)
        admin_email = f"admin_{str(uuid.uuid4())[:8]}@example.com"
        admin = User()
        admin.first_name = "Admin"
        admin.last_name = "User"
        admin.email = admin_email
        admin.password = "adminpass123"
        admin.is_admin = True
        
        db.session.add(admin)
        db.session.commit()
        
        cls.admin_id = admin.id
        cls.admin_email = admin_email

    def setUp(self):
        """Set up the test client."""
        # Get admin token
        response = self.app.post('/api/v1/auth/login', json={
            "email": self.admin_email,
            "password": "adminpass123"
        })
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.admin_token = response_data['access_token']
        
        # Generate a unique email for each test run
        unique_id = str(uuid.uuid4())[:8]
        self.test_email = f"test_{unique_id}@example.com"
        self.test_password = "password123"
        
        # Create user and get ID using admin credentials
        self.user_id = self.create_user()
        # Get regular user authentication token
        self.token = self.login()

    def create_user(self):
        """Create a new user with unique email using admin token."""
        headers = {'Authorization': f'Bearer {self.admin_token}'}
        response = self.app.post('/api/v1/users/', 
            json={
                "email": self.test_email,
                "password": self.test_password,
                "first_name": "Test",
                "last_name": "User"
            },
            headers=headers)
        
        self.assertEqual(response.status_code, 200)  # API returns 200 for successful user creation
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
        
        # Amenity creation requires admin privileges
        headers = {'Authorization': f'Bearer {self.admin_token}'}
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
        
        # Regular users can create their own places
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

    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests."""
        # Clean up test admin user
        admin = User.query.get(cls.admin_id)
        if admin:
            db.session.delete(admin)
            db.session.commit()
        
        cls.app_context.pop()


if __name__ == '__main__':
    unittest.main()