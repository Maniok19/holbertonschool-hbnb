#!/usr/bin/python3 
import unittest
import uuid
import json
from app import create_app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.token = self.get_token()

    def create_test_user(self):
        user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'zozoz@zozo.zo'
        }
        response = self.client.post('/api/v1/users/', json=user_data)
        self.assertEqual(response.status_code, 400)

    def get_token(self):
        # Replace with actual login credentials
        login_data = {
            'email': 'test@example.com',
            'password': 'password'
        }
        response = self.client.post('/api/v1/auth/login', json=login_data)
        self.assertEqual(response.status_code, 200)
        return response.json['token']

    def test_get_users(self):
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        response = self.client.get('/api/v1/users/', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])



if __name__ == '__main__':
    unittest.main()