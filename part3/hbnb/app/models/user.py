import re
from flask_bcrypt import Bcrypt
from app.models.base import BaseModel

bcrypt = Bcrypt()


class User(BaseModel):
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.password = password

    def checking(self):
        if not self.first_name or len(self.first_name) > 50:
            raise ValueError(
                "First name is required and must be <= 50 characters"
            )
        if not self.last_name or len(self.last_name) > 50:
            raise ValueError(
                "Last name is required and must be <= 50 characters"
            )
        if not self.email or not self.is_valid_email(self.email):
            raise ValueError("Valid email is required")

    @staticmethod
    def is_valid_email(email):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email) is not None

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
