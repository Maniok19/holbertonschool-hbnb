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

    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests."""
        db.session.remove()
        cls.app_context.pop()

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

        # Create another user for ownership tests
        unique_id = str(uuid.uuid4())[:8]
        self.other_email = f"other_{unique_id}@example.com"
        self.other_password = "otherpass123"
        self.other_user_id = self.create_other_user()
        self.other_token = self.login_other_user()

        self.place_id = self.create_place()
        self.amenity_id = self.create_amenity()
        self.review_id = self.create_review()

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
        
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        self.assertTrue('id' in response_data)
        return response_data['id']

    def create_other_user(self):
        """Create another user for testing ownership restrictions."""
        # Get a fresh token each time this method is called
        response = self.app.post('/api/v1/auth/login', json={
            "email": self.admin_email,
            "password": "adminpass123"
        })
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        fresh_admin_token = response_data['access_token']
        
        headers = {'Authorization': f'Bearer {fresh_admin_token}'}
        response = self.app.post('/api/v1/users/', 
            json={
                "email": self.other_email,
                "password": self.other_password,
                "first_name": "Other",
                "last_name": "User"
            },
            headers=headers)
        
        if response.status_code != 201:
            print(f"Failed to create other user: {response.data.decode('utf-8')}")

        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        return response_data['id']

    def login(self):
        """Test logging in."""
        response = self.app.post('/api/v1/auth/login', json={
            "email": self.test_email,
            "password": self.test_password
        })
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        return response_data['access_token']
    
    def login_other_user(self):
        """Login as the other test user."""
        response = self.app.post('/api/v1/auth/login', json={
            "email": self.other_email,
            "password": self.other_password
        })
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        return response_data['access_token']

    def create_place(self):
        """Create a new place using the user token."""
        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.app.post('/api/v1/places/', 
            json={
                'title': 'My Place',
                'description': 'A place to stay',
                'price': 100.00,
                'latitude': 37.7749,
                'longitude': -122.4194,
                'owner_id': self.user_id,
                'amenities': []
            },
            headers=headers)
        if response.status_code != 201:
            print(f"Failed to create place: {response.data.decode('utf-8')}")
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        return response_data['id']
    
    def create_amenity(self):
        """Create a new amenity using admin token."""
        headers = {'Authorization': f'Bearer {self.admin_token}'}
        response = self.app.post('/api/v1/amenities/', 
            json={
                'name': f"Test Amenity {uuid.uuid4()}"
            },
            headers=headers)
        
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        return response_data['id']
    
    def create_review(self):
        """Create a test review."""
        # First create a place by other user that we can review
        headers = {'Authorization': f'Bearer {self.other_token}'}
        response = self.app.post('/api/v1/places/', 
            json={
                'title': f"Place to review {uuid.uuid4()}",
                'description': 'A place for testing reviews',
                'price': 120.00,
                'latitude': 40.7128,
                'longitude': -74.0060,
                'owner_id': self.other_user_id,
                'amenities': []
            },
            headers=headers)
        
        self.assertEqual(response.status_code, 201)
        other_place_id = json.loads(response.data)['id']
        
        # Now review the other user's place
        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.app.post('/api/v1/reviews/', 
            json={
                'text': f"Great place to stay {uuid.uuid4()}",
                'rating': 5,
                'place_id': other_place_id,
                'user_id': self.user_id
            },
            headers=headers)
        
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        return response_data['id']

    # Authentication tests
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        response = self.app.post('/api/v1/auth/login', json={
            "email": self.test_email,
            "password": "wrongpassword"
        })
        self.assertEqual(response.status_code, 401)
    
    def test_access_protected_route_without_token(self):
        """Test accessing protected route without token."""
        response = self.app.get('/api/v1/protected/')
        self.assertEqual(response.status_code, 401)
    
    def test_access_protected_route_with_token(self):
        """Test accessing protected route with valid token."""
        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.app.get('/api/v1/protected/', headers=headers)
        self.assertEqual(response.status_code, 200)
    
    # User tests
    def test_create_user(self):
        """Test creating a user (admin only)."""
        headers = {'Authorization': f'Bearer {self.admin_token}'}
        response = self.app.post('/api/v1/users/', 
            json={
                "email": f"new_{uuid.uuid4()}@example.com",
                "password": "newpass123",
                "first_name": "New",
                "last_name": "User"
            },
            headers=headers)
        
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        self.assertTrue('id' in response_data)
    
    def test_create_user_non_admin(self):
        """Test creating a user without admin privileges."""
        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.app.post('/api/v1/users/', 
            json={
                "email": f"new_{uuid.uuid4()}@example.com",
                "password": "newpass123",
                "first_name": "New",
                "last_name": "User"
            },
            headers=headers)
        
        self.assertEqual(response.status_code, 403)
    
    def test_get_all_users(self):
        """Test getting all users (no auth required)."""
        response = self.app.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        users = json.loads(response.data)
        self.assertIsInstance(users, list)
    
    def test_get_user_by_id(self):
        """Test getting a specific user."""
        response = self.app.get(f'/api/v1/users/{self.user_id}')
        self.assertEqual(response.status_code, 200)
        user = json.loads(response.data)
        self.assertEqual(user['id'], self.user_id)
    
    def test_get_nonexistent_user(self):
        """Test getting a user that doesn't exist."""
        response = self.app.get('/api/v1/users/nonexistent-id')
        self.assertEqual(response.status_code, 404)
    
    def test_update_own_user_details(self):
        """Test updating own user details."""
        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.app.put(f'/api/v1/users/{self.user_id}', 
            json={
                "first_name": "Updated",
                "last_name": "Name"
            },
            headers=headers)
        
        self.assertEqual(response.status_code, 200)
        user = json.loads(response.data)
        self.assertEqual(user['first_name'], "Updated")
    
    def test_update_other_user_details(self):
        """Test updating another user's details (should fail)."""
        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.app.put(f'/api/v1/users/{self.other_user_id}', 
            json={
                "first_name": "Hacked",
                "last_name": "Account"
            },
            headers=headers)
        
        self.assertEqual(response.status_code, 403)
    
    def test_update_user_password_as_admin(self):
        """Test updating user's password as admin."""
        headers = {'Authorization': f'Bearer {self.admin_token}'}
        response = self.app.put(f'/api/v1/users/{self.user_id}', 
            json={
                "password": "newpassword123"
            },
            headers=headers)
        
        self.assertEqual(response.status_code, 200)
    
    def test_update_invalid_email_format(self):
        """Test updating user with invalid email format."""
        headers = {'Authorization': f'Bearer {self.admin_token}'}
        response = self.app.put(f'/api/v1/users/{self.user_id}', 
            json={
                "email": "not-an-email"
            },
            headers=headers)
        
        self.assertEqual(response.status_code, 400)
    
    def test_delete_user_as_admin(self):
        """Test deleting a user as admin."""
        # First create a user to delete
        headers = {'Authorization': f'Bearer {self.admin_token}'}
        response = self.app.post('/api/v1/users/', 
            json={
                "email": f"delete_{uuid.uuid4()}@example.com",
                "password": "deletepass123",
                "first_name": "Delete",
                "last_name": "User"
            },
            headers=headers)
        
        user_id = json.loads(response.data)['id']
        
        # Now delete the user
        response = self.app.delete(f'/api/v1/users/{user_id}', headers=headers)
        self.assertEqual(response.status_code, 200)
    
    def test_delete_user_as_non_admin(self):
        """Test deleting a user without admin privileges."""
        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.app.delete(f'/api/v1/users/{self.other_user_id}', headers=headers)
        self.assertEqual(response.status_code, 403)
    
    def test_delete_own_account(self):
        """Test user deleting their own account."""
        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.app.delete(f'/api/v1/users/{self.user_id}', headers=headers)
        self.assertEqual(response.status_code, 200)
    
    # Amenity tests
    def test_create_amenity(self):
        """Test creating a new amenity."""
        headers = {'Authorization': f'Bearer {self.admin_token}'}
        response = self.app.post('/api/v1/amenities/', 
            json={
                'name': f"New Amenity {uuid.uuid4()}"
            },
            headers=headers)
        
        self.assertEqual(response.status_code, 201)
    
    def test_create_amenity_non_admin(self):
        """Test creating an amenity without admin privileges."""
        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.app.post('/api/v1/amenities/', 
            json={
                'name': f"New Amenity {uuid.uuid4()}"
            },
            headers=headers)
        
        self.assertEqual(response.status_code, 403)
    
    def test_get_all_amenities(self):
        """Test getting all amenities."""
        response = self.app.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        amenities = json.loads(response.data)
        self.assertIsInstance(amenities, list)
    
    def test_get_amenity_by_id(self):
        """Test getting a specific amenity."""
        response = self.app.get(f'/api/v1/amenities/{self.amenity_id}')
        self.assertEqual(response.status_code, 200)
        amenity = json.loads(response.data)
        self.assertEqual(amenity['id'], self.amenity_id)
    
    def test_update_amenity(self):
        """Test updating an amenity (admin only)."""
        headers = {'Authorization': f'Bearer {self.admin_token}'}
        new_name = f"Updated Amenity {uuid.uuid4()}"
        response = self.app.put(f'/api/v1/amenities/{self.amenity_id}', 
            json={
                'name': new_name
            },
            headers=headers)
        
        self.assertEqual(response.status_code, 200)
    
    def test_update_amenity_non_admin(self):
        """Test updating an amenity without admin privileges."""
        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.app.put(f'/api/v1/amenities/{self.amenity_id}', 
            json={
                'name': "Can't update this"
            },
            headers=headers)
        
        self.assertEqual(response.status_code, 403)
    
    def test_delete_amenity(self):
        """Test deleting an amenity (admin only)."""
        # First create an amenity to delete
        headers = {'Authorization': f'Bearer {self.admin_token}'}
        response = self.app.post('/api/v1/amenities/', 
            json={
                'name': f"Delete Me {uuid.uuid4()}"
            },
            headers=headers)
        
        amenity_id = json.loads(response.data)['id']
        
        # Now delete it
        response = self.app.delete(f'/api/v1/amenities/{amenity_id}', headers=headers)
        self.assertEqual(response.status_code, 204)
    
    # Place tests
    def test_create_place(self):
        """Test creating a new place."""
        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.app.post('/api/v1/places/', 
            json={
                'title': f"New Place {uuid.uuid4()}",
                'description': 'A nice place to stay',
                'price': 150.00,
                'latitude': 40.7128,
                'longitude': -74.0060,
                'owner_id': self.user_id,
                'amenities': []
            },
            headers=headers)
        
        self.assertEqual(response.status_code, 201)
    
    def test_create_place_for_other_user(self):
        """Test creating a place for another user (should fail)."""
        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.app.post('/api/v1/places/', 
            json={
                'title': f"Other's Place {uuid.uuid4()}",
                'description': 'This should fail',
                'price': 150.00,
                'latitude': 40.7128,
                'longitude': -74.0060,
                'owner_id': self.other_user_id,
                'amenities': []
            },
            headers=headers)
        
        self.assertEqual(response.status_code, 403)
    
    def test_create_place_invalid_data(self):
        """Test creating a place with invalid data."""
        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.app.post('/api/v1/places/', 
            json={
                'title': f"Invalid Place {uuid.uuid4()}",
                'description': 'Invalid price',
                'price': -10.00,  # Negative price should fail
                'latitude': 40.7128,
                'longitude': -74.0060,
                'owner_id': self.user_id,
                'amenities': []
            },
            headers=headers)
        
        self.assertEqual(response.status_code, 400)
    
    def test_get_all_places(self):
        """Test getting all places."""
        response = self.app.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)
        places = json.loads(response.data)
        self.assertIsInstance(places, list)
    
    def test_get_place_by_id(self):
        """Test getting a specific place."""
        response = self.app.get(f'/api/v1/places/{self.place_id}')
        self.assertEqual(response.status_code, 200)
        place = json.loads(response.data)
        self.assertEqual(place['id'], self.place_id)
    
    def test_update_own_place(self):
        """Test updating own place."""
        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.app.put(f'/api/v1/places/{self.place_id}', 
            json={
                'title': f"Updated Place {uuid.uuid4()}",
                'price': 200.00
            },
            headers=headers)
        self.assertEqual(response.status_code, 200)
    
    def test_update_other_user_place(self):
        """Test updating another user's place."""
        # First create a place for the other user
        headers = {'Authorization': f'Bearer {self.other_token}'}
        response = self.app.post('/api/v1/places/', 
            json={
                'title': f"Other's Place {uuid.uuid4()}",
                'description': 'Another place',
                'price': 120.00,
                'latitude': 40.7128,
                'longitude': -74.0060,
                'owner_id': self.other_user_id,
                'amenities': []
            },
            headers=headers)
        
        other_place_id = json.loads(response.data)['id']
        
        # Now try to update it with the first user's token
        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.app.put(f'/api/v1/places/{other_place_id}', 
            json={
                'title': 'Tried to hack',
                'price': 1.00
            },
            headers=headers)
        
        self.assertEqual(response.status_code, 403)
    
    def test_update_place_admin(self):
        """Test updating any place as admin."""
        headers = {'Authorization': f'Bearer {self.admin_token}'}
        response = self.app.put(f'/api/v1/places/{self.place_id}', 
            json={
                'title': f"Admin Updated {uuid.uuid4()}",
                'price': 300.00
            },
            headers=headers)
        
        self.assertEqual(response.status_code, 200)
    
    def test_delete_place(self):
        """Test deleting a place."""
        # First create a place to delete
        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.app.post('/api/v1/places/', 
            json={
                'title': f"Delete Me Place {uuid.uuid4()}",
                'description': 'To be deleted',
                'price': 100.00,
                'latitude': 40.7128,
                'longitude': -74.0060,
                'owner_id': self.user_id,
                'amenities': []
            },
            headers=headers)
        
        place_id = json.loads(response.data)['id']
        
        # Now delete it as admin since only admins can delete places
        admin_headers = {'Authorization': f'Bearer {self.admin_token}'}
        response = self.app.delete(f'/api/v1/places/{place_id}', headers=admin_headers)
        self.assertEqual(response.status_code, 200)
    
    # Review tests
    def test_create_review(self):
        """Test creating a new review."""
        # First create a place by other user that we can review
        headers = {'Authorization': f'Bearer {self.other_token}'}
        response = self.app.post('/api/v1/places/', 
            json={
                'title': f"Place to review {uuid.uuid4()}",
                'description': 'A place for testing reviews',
                'price': 120.00,
                'latitude': 40.7128,
                'longitude': -74.0060,
                'owner_id': self.other_user_id,
                'amenities': []
            },
            headers=headers)
        
        self.assertEqual(response.status_code, 201)
        other_place_id = json.loads(response.data)['id']
        
        # Now review the other user's place
        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.app.post('/api/v1/reviews/', 
            json={
                'text': f"Great review {uuid.uuid4()}",
                'rating': 4,
                'place_id': other_place_id,
                'user_id': self.user_id
            },
            headers=headers)
        
        self.assertEqual(response.status_code, 201)
    
    def test_create_invalid_review_rating(self):
        """Test creating a review with an invalid rating."""
        # First create a place by other user that we can review
        headers = {'Authorization': f'Bearer {self.other_token}'}
        response = self.app.post('/api/v1/places/', 
            json={
                'title': f"Place for bad rating {uuid.uuid4()}",
                'description': 'A place for testing invalid reviews',
                'price': 120.00,
                'latitude': 40.7128,
                'longitude': -74.0060,
                'owner_id': self.other_user_id,
                'amenities': []
            },
            headers=headers)
        
        self.assertEqual(response.status_code, 201)
        other_place_id = json.loads(response.data)['id']
        
        # Now try to post an invalid review
        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.app.post('/api/v1/reviews/', 
            json={
                'text': 'Bad rating',
                'rating': 6,  # Rating should be 1-5
                'place_id': other_place_id,
                'user_id': self.user_id
            },
            headers=headers)
        
        self.assertEqual(response.status_code, 400)
    
    def test_get_all_reviews(self):
        """Test getting all reviews."""
        response = self.app.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)
        reviews = json.loads(response.data)
        self.assertIsInstance(reviews, list)
    
    def test_get_review_by_id(self):
        """Test getting a specific review."""
        response = self.app.get(f'/api/v1/reviews/{self.review_id}')
        self.assertEqual(response.status_code, 200)
        review = json.loads(response.data)
        self.assertEqual(review['id'], self.review_id)
    
    def test_update_own_review(self):
        """Test updating own review."""
        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.app.put(f'/api/v1/reviews/{self.review_id}', 
            json={
                'text': f"Updated review {uuid.uuid4()}",
                'rating': 3,
                'place_id': self.place_id,
                'user_id': self.user_id
            },
            headers=headers)
        self.assertEqual(response.status_code, 200)
    
    def test_delete_review_admin(self):
        """Test deleting a review as admin."""
        headers = {'Authorization': f'Bearer {self.admin_token}'}
        response = self.app.delete(f'/api/v1/reviews/{self.review_id}', headers=headers)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()