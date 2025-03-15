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

    def test_create_user(self):
        """Test creating a new user."""
        response = self.app.post('/api/v1/users/', json={
            "email": "mano@mano.mano",
            "password": "manomano",
            "first_name": "mano",
            "last_name": "mano"
        })
        self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
    unittest.main()