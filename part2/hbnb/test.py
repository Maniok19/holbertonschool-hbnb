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
        # self.review_id = self.create_test_review()

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

    
    # test create

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

    # test create invalid data

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
            'first_name': '',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
        })
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data


    def test_create_place_invalid_data(self):
        response = self.client.post('/api/v1/places/', json={})
        self.assertEqual(response.status_code, 400, f"Expected 400 but got {response.status_code}, response: {response.json}")
        

    def test_create_amenity_invalid_data(self):
        response = self.client.post('/api/v1/amenities/', json={})
        self.assertEqual(response.status_code, 400, f"Expected 400 but got {response.status_code}, response: {response.json}")
        

    # test get

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

    # test get by id

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


    # test get by id invalid data

    def test_get_user_by_id_invalid_data(self):
        response = self.client.get('/api/v1/users/invalid_id')
        self.assertEqual(response.status_code, 404)

    def test_get_place_by_id_invalid_data(self):
        pass

    def test_get_amenity_by_id_invalid_data(self):
        pass

    def test_get_review_by_id_invalid_data(self):
        pass

    # test update

    def test_update_user(self):
        pass

    def test_update_place(self):
        pass

    def test_update_amenity(self):
        pass

    def test_update_review(self):
        pass

    # test update invalid data

    def test_update_user_invalid_data(self):
        pass

    def test_update_place_invalid_data(self):
        pass

    def test_update_amenity_invalid_data(self):
        pass

    def test_update_review_invalid_data(self):
        pass

    # test delete

    def test_delete_review(self):
        pass

    # special tests place

    def test_create_place_invalid_owner_id(self):
        pass

    def test_create_place_invalid_price(self):
        pass

    def test_create_place_invalid_latitude(self):
        pass

    def test_create_place_invalid_longitude(self):
        pass

    # special tests user

    def test_create_user_invalid_email(self):
        pass

    # special tests amenity

    # special tests review

    def test_create_review_invalid_user_id(self):
        response = self.client.post('/api/v1/reviews/', json={
            "user_id": "abc",
            "place_id": self.place_id,
            "text": "rrrr",
            "rating": 2
        })
        self.assertEqual(response.status_code, 404, f"Expected 400 but got {response.status_code}, response: {response.json}") 

    def test_create_review_invalid_place_id(self):
        pass

    def test_add_amenity_to_place(self):
        if self.amenity_id:
            response = self.client.post(f'/api/v1/places/{self.place_id}/amenities/{self.amenity_id}')
            self.assertEqual(response.status_code, 200, f"Error adding amenity to place: {response.json}")
        else:
            self.fail("Amenity ID is not valid")

    def test_get_reviews(self):
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200, f"Error retrieving reviews: {response.json}")

if __name__ == '__main__':
    unittest.main()
