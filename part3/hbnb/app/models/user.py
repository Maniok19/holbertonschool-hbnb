import re
from flask_bcrypt import Bcrypt
from app.models.base import BaseModel
from app import db, bcrypt
import uuid
from .base import BaseModel

bcrypt = Bcrypt()


class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

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

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)