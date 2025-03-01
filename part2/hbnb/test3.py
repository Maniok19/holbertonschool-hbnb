#!/usr/bin/python3 
import unittest
import uuid
import json
from app import create_app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.user_id = self.create_test_user()
        self.place_id = self.create_test_place()
        self.amenity_id = self.create_test_amenity()
        self.review_id = self.create_test_review()

    # CREATE TEST
    def create_test_user(self):
        email = f"test_{uuid.uuid4()}@example.com"
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Test",
            "last_name": "User",
            "email": email
        })
        self.assertEqual(response.status_code, 201, f"Error creating test user: {response.json}")
        return response.json.get("id")

    def create_test_place(self):
        place_title = f"Test Place {uuid.uuid4()}"
        response = self.client.post('/api/v1/places/', json={
            "title": place_title,
            "description": "A test place description",
            "price": 100.0,
            "latitude": 45.0,
            "longitude": -75.0,
            "owner_id": self.user_id,
            "amenities": []  # Liste vide d'amenités
        })
        self.assertEqual(response.status_code, 201, f"Error creating test place: {response.json}")
        return response.json.get("id")

    def create_test_amenity(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": "Test Amenity"
        })
        self.assertEqual(response.status_code, 201, f"Error creating amenity: {response.json}")
        return response.json.get("id")
    
    def create_test_review(self):
        response = self.client.post('/api/v1/reviews/', json={
            "user_id": self.user_id,
            "place_id": self.place_id,
            "text": "Great place to stay!",
            "rating": 5  # Ajout du champ 'rating'
        })
        self.assertEqual(response.status_code, 201, f"Error creating review: {response.json}")
        return response.json.get("id")

    def test_create_review(self):
        response = self.client.post('/api/v1/reviews/', json={
            "user_id": self.user_id,
            "place_id": self.place_id,
            "text": "Great place to stay!",
            "rating": 5  # Ajout du champ 'rating'
        })
        self.assertEqual(response.status_code, 201, f"Error creating review: {response.json}")

    def test_create_user(self):
        email = f"test_@example.com"
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Test",
            "last_name": "User",
            "email": email
        })
        self.assertEqual(response.status_code, 201, f"Error creating test user: {response.json}")

    def test_create_place(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "place_title",
            "description": "A test place description",
            "price": 100.0,
            "latitude": 45.0,
            "longitude": -75.0,
            "owner_id": self.user_id,
            "amenities": []
        })
        self.assertEqual(response.status_code, 201, f"Error creating test place: {response.json}")

    def test_create_amenity(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": "Test Amenity"
        })
        self.assertEqual(response.status_code, 201, f"Error creating amenity: {response.json}")

    # POST INVALID DATA

    def test_create_review_invalid_data(self):
        response = self.client.post('/api/v1/reviews/', json={
            "user_i": "abc",
            "plae_id": self.place_id,
            "tet": "ffff",
            "ratng": 0
        })
        self.assertEqual(response.status_code, 400, f"Expected 400 but got {response.status_code}, response: {response.json}")

    def test_create_user_invalid_data(self):
        response = self.client.post('/api/v1/users/', json={
            'first_nme': '',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_data(self):
        response = self.client.post('/api/v1/places/', json={
            "tile": "place_title",
            "description": "A test place description",
            "price": 100.0,
            "latitude": 45.0,
            "longitude": -75.0,
            "owner_id": self.user_id,
            "amenities": []
        })
        self.assertEqual(response.status_code, 400, f"Expected 400 but got {response.status_code}, response: {response.json}")

    def test_create_amenity_invalid_data(self):
        response = self.client.post('/api/v1/amenities/', json={})
        self.assertEqual(response.status_code, 400, f"Expected 400 but got {response.status_code}, response: {response.json}")

    # GET TEST
    def test_get_users(self):
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200, f"Error retrieving users: {response.json}")

    def test_get_places(self):
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200, f"Error retrieving places: {response.json}")

    def test_get_amenities(self):
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200, f"Error retrieving amenities: {response.json}")

    def test_get_reviews(self):
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200, f"Error retrieving reviews: {response.json}")

    # GET BY ID TEST
    def test_get_user_by_id(self):
        response = self.client.get(f'/api/v1/users/{self.user_id}')
        self.assertEqual(response.status_code, 200, f"Error retrieving user: {response.json}")

    def test_get_place_by_id(self):
        response = self.client.get(f'/api/v1/places/{self.place_id}')
        self.assertEqual(response.status_code, 200, f"Error retrieving place: {response.json}")

    def test_get_amenity_by_id(self):
        response = self.client.get(f'/api/v1/amenities/{self.amenity_id}')
        self.assertEqual(response.status_code, 200, f"Error retrieving amenity: {response.json}")

    def test_get_review_by_id(self):
        response = self.client.get(f'/api/v1/reviews/{self.review_id}')
        self.assertEqual(response.status_code, 200, f"Error retrieving review: {response.json}")

    # GET BY ID INVALID DATA

    def test_get_user_by_id_invalid_data(self):
        response = self.client.get('/api/v1/users/invalid_id')
        self.assertEqual(response.status_code, 404)

    def test_get_place_by_id_invalid_data(self):
        response = self.client.get('/api/v1/places/invalid_id')
        self.assertEqual(response.status_code, 404)

    def test_get_amenity_by_id_invalid_data(self):
        response = self.client.get('/api/v1/amenities/invalid_id')
        self.assertEqual(response.status_code, 404)

    def test_get_review_by_id_invalid_data(self):
        response = self.client.get('/api/v1/reviews/invalid_id')
        self.assertEqual(response.status_code, 404)

    # Test updating a user with one field
    """    # Test updating a user with one field
    def test_update_user_one_field(self):
        response = self.client.put(f'/api/v1/users/{self.user_id}', json={
            "first_name": "Updated"
        })
        self.assertEqual(response.status_code, 200, f"Error updating user: {response.json}")

    # Test updating an amenity with one field
    def test_update_amenity_one_field(self):
        response = self.client.put(f'/api/v1/amenities/{self.amenity_id}', json={
            "name": "Test Amenity"
        })
        self.assertEqual(response.status_code, 200)

    # Test updating a review with one field
    def test_update_review_one_field(self):
        response = self.client.put(f'/api/v1/reviews/{self.review_id}', json={
            "text": "Great place to stay!"
        })
        self.assertEqual(response.status_code, 200)

    # Test updating a place with one field
    def test_update_place_one_field(self):
        response = self.client.put(f'/api/v1/places/{self.place_id}', json={
            "title": "Test Place"
        })
        self.assertEqual(response.status_code, 200)"""

    # TEST UPDATE

    def test_update_place(self):
        response = self.client.put(f'/api/v1/places/{self.place_id}', json={
            "title": "Test Place",
            "description": "A test place description",
            "price": 100.0,
            "latitude": 45.0,
            "longitude": -75.0,
            "owner_id": self.user_id,
            "amenities": []
        })
        self.assertEqual(response.status_code, 200)

    def test_update_review(self):
        response = self.client.put(f'/api/v1/reviews/{self.review_id}', json={
            "user_id": self.user_id,
            "place_id": self.place_id,
            "text": "Great place to stay!",
            "rating": 5
        })
        self.assertEqual(response.status_code, 200)

    def test_update_amenity(self):
        response = self.client.put(f'/api/v1/amenities/{self.amenity_id}', json={
            "name": "Test Amenity"
        })
        self.assertEqual(response.status_code, 200)

    def test_update_user(self):
        response = self.client.put(f'/api/v1/users/{self.user_id}', json={
            "first_name": "Updated",
            "last_name": "User",
            "email": "abc@abc.abc"
        })
        self.assertEqual(response.status_code, 200)

    # UPDATE INVALID DATA

    def test_update_user_invalid_data(self):
        response = self.client.put(f'/api/v1/users/{self.user_id}', json={
            "name": "Test",
            "last_name": "User",
            "emil": "aa@aa.aa"
        })
        self.assertEqual(response.status_code, 400)

    def test_update_place_invalid_data(self):
        response = self.client.put(f'/api/v1/places/{self.place_id}', json={
            "invalid": "Test Place",
            "description": "A test place description",
            "price": 100.0,
            "latitude": 200,
            "longitude": -75.0,
            "owner_id": self.user_id,
            "amenities": []
        })
        self.assertEqual(response.status_code, 400)

    def test_update_amenity_invalid_data(self):
        response = self.client.put(f'/api/v1/amenities/{self.amenity_id}', json={
            "invalid": "aaa"
        })
        self.assertEqual(response.status_code, 400)

    def test_update_review_invalid_data(self):
        response = self.client.put(f'/api/v1/reviews/{self.review_id}', json={
            "invalid": "aaa"
        })
        self.assertEqual(response.status_code, 400)

    #invalid data side user

    # Test updating a user with invalid data (empty first_name)
    def test_update_user_invalid_data_empty_first_name(self):
        response = self.client.put(f'/api/v1/users/{self.user_id}', json={
            "first_name": "",
            "last_name": "User",
            "email": "updated@example.com"
        })
        self.assertEqual(response.status_code, 400, f"Expected 400 but got {response.status_code}, response: {response.json}")

    # Test updating a user with invalid data (empty last_name)
    def test_update_user_invalid_data_empty_last_name(self):
        response = self.client.put(f'/api/v1/users/{self.user_id}', json={
            "first_name": "Updated",
            "last_name": "",
            "email": "updated@example.com"
        })
        self.assertEqual(response.status_code, 400, f"Expected 400 but got {response.status_code}, response: {response.json}")

    # Test updating a user with invalid data (empty email)
    def test_update_user_invalid_data_empty_email(self):
        response = self.client.put(f'/api/v1/users/{self.user_id}', json={
            "first_name": "Updated",
            "last_name": "User",
            "email": ""
        })
        self.assertEqual(response.status_code, 400, f"Expected 400 but got {response.status_code}, response: {response.json}")


	# Test updating a place with invalid data (empty title)
    def test_update_place_invalid_data_empty_title(self):
        response = self.client.put(f'/api/v1/places/{self.place_id}', json={
            "title": "",
            "description": "A test place description",
            "price": 100.0,
            "latitude": 45.0,
            "longitude": -75.0,
            "owner_id": self.user_id,
            "amenities": []
        })
        self.assertEqual(response.status_code, 400, f"Expected 400 but got {response.status_code}, response: {response.json}")

    # Test updating a place with invalid data (invalid latitude)
    def test_update_place_invalid_data_invalid_latitude(self):
        response = self.client.put(f'/api/v1/places/{self.place_id}', json={
            "title": "Test Place",
            "description": "A test place description",
            "price": 100.0,
            "latitude": 200,  # Invalid latitude
            "longitude": -75.0,
            "owner_id": self.user_id,
            "amenities": []
        })
        self.assertEqual(response.status_code, 400, f"Expected 400 but got {response.status_code}, response: {response.json}")

    # Test updating a place with invalid data (invalid longitude)
    def test_update_place_invalid_data_invalid_longitude(self):
        response = self.client.put(f'/api/v1/places/{self.place_id}', json={
            "title": "Test Place",
            "description": "A test place description",
            "price": 100.0,
            "latitude": 45.0,
            "longitude": 200,  # Invalid longitude
            "owner_id": self.user_id,
            "amenities": []
        })
        self.assertEqual(response.status_code, 400, f"Expected 400 but got {response.status_code}, response: {response.json}")

    # Test updating a place with invalid data (negative price)
    def test_update_place_invalid_data_negative_price(self):
        response = self.client.put(f'/api/v1/places/{self.place_id}', json={
            "title": "Test Place",
            "description": "A test place description",
            "price": -10.0,  # Negative price
            "latitude": 45.0,
            "longitude": -75.0,
            "owner_id": self.user_id,
            "amenities": []
        })
        self.assertEqual(response.status_code, 400, f"Expected 400 but got {response.status_code}, response: {response.json}")

    # Test updating a place with invalid data (empty owner_id)
    def test_update_place_invalid_data_empty_owner_id(self):
        response = self.client.put(f'/api/v1/places/{self.place_id}', json={
            "title": "Test Place",
            "description": "A test place description",
            "price": 100.0,
            "latitude": 45.0,
            "longitude": -75.0,
            "owner_id": "",  # Empty owner_id
            "amenities": []
        })
        self.assertEqual(response.status_code, 400, f"Expected 400 but got {response.status_code}, response: {response.json}")
    
	
    # DELETE TEST

    def test_delete_review(self):
        response = self.client.delete(f'/api/v1/reviews/{self.review_id}')
        self.assertEqual(response.status_code, 200)

    # SPECIAL CONDITIONS TESTS

    def test_create_user_duplicate_email(self):
        email = f"test_{uuid.uuid4()}@example.com"
        self.client.post('/api/v1/users/', json={
            "first_name": "Test",
            "last_name": "User",
            "email": email
        })
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Test",
            "last_name": "User",
            "email": email
        })
        self.assertEqual(response.status_code, 400, f"Error creating test user: {response.json}")

    def test_create_user_with_2_at(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Test",
            "last_name": "User",
            "email": "test@@example.com"})
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_latitude(self):
        response = self.client.post('/api/v1/places/', json={"title": "Test Place", "latitude": 200})
        self.assertEqual(response.status_code, 400)

    def test_create_place_negative_price(self):
        response = self.client.post('/api/v1/places/', json={"title": "Test Place", "price": -10})
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_longitude(self):
        response = self.client.post('/api/v1/places/', json={"title": "Test Place", "longitude": 200})
        self.assertEqual(response.status_code, 400)

    def test_create_user_invalid_email(self):
        response = self.client.post('/api/v1/users/', json={"first_name": "Test", "email": "invalid"})
        self.assertEqual(response.status_code, 400)
    
    def test_create_review_zero_rating(self):
        response = self.client.post('/api/v1/reviews/', json={"user_id": self.user_id, "place_id": self.place_id, "text": "rrrr", "rating": 0})
        self.assertEqual(response.status_code, 400)

    # ID NOT FOUND TESTS
    
    def test_create_place_unfound_user(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "description": "A test place description",
            "price": 100.0,
            "latitude": 45.0,
            "longitude": -75.0,
            "owner_id": "abc",
            "amenities": []
        })
        self.assertEqual(response.status_code, 404)
    
    def test_create_review_unfound_user_id(self):
        response = self.client.post('/api/v1/reviews/', json={
            "user_id": "abc",
            "place_id": self.place_id,
            "text": "rrrr",
            "rating": 2
        })
        self.assertEqual(response.status_code, 404, f"Expected 400 but got {response.status_code}, response: {response.json}")

    def test_create_review_unfound_place_id(self):
        response = self.client.post('/api/v1/reviews/', json={
            "user_id": self.user_id,
            "place_id": "abc",
            "text": "rrrr",
            "rating": 2
        })
        self.assertEqual(response.status_code, 404, f"Expected 400 but got {response.status_code}, response: {response.json}")

if __name__ == '__main__':
    unittest.main()