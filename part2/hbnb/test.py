#!/usr/bin/python3
import unittest
import uuid
from app import create_app

class TestAPI(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.user_id = self.create_test_user()
        self.place_id = self.create_test_place()

    def tearDown(self):
        self.delete_test_user()
        self.delete_test_place()

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
        # Générer un titre unique pour chaque test
        title = f"Test Place {uuid.uuid4()}"
        response = self.client.post('/api/v1/places/', json={
            "title": title,
            "description": "A test place description",
            "price": 100.0,
            "latitude": 45.0,
            "longitude": -75.0,
            "owner_id": self.user_id,
            "amenities": []  # Ajout de l'attribut requis (même vide)
        })
        self.assertEqual(response.status_code, 201, f"Error creating test place: {response.json}")
        return response.json.get("id")

    def delete_test_user(self):
        self.client.delete(f'/api/v1/users/{self.user_id}')

    def delete_test_place(self):
        self.client.delete(f'/api/v1/places/{self.place_id}')

    def test_create_review(self):
        # Ajouter le champ 'rating' pour éviter l'erreur
        response = self.client.post('/api/v1/reviews/', json={
            "user_id": self.user_id,
            "place_id": self.place_id,
            "text": "Great place to stay!",
            "rating": 5  # Champ requis
        })
        self.assertEqual(response.status_code, 201, f"Error creating review: {response.json}")

    def test_create_review_invalid_data(self):
        # Tester avec des données invalides
        response = self.client.post('/api/v1/reviews/', json={
            "user_id": "",  # ID utilisateur invalide
            "place_id": self.place_id,
            "text": "",  # Texte vide
            "rating": 5  # Ajouter un champ 'rating' même pour les données invalides
        })
        self.assertEqual(response.status_code, 400, f"Expected 400 but got {response.status_code}, response: {response.json}")

    def test_get_reviews(self):
        # Vérifier si des avis existent pour la place
        response = self.client.get(f'/api/v1/places/{self.place_id}/reviews')
        self.assertEqual(response.status_code, 200, f"Error retrieving reviews: {response.json}")

if __name__ == '__main__':
    unittest.main()