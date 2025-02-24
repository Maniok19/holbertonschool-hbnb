from app.models.base import BaseModel


class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin


    def checking(self):
        if not self.first_name or len(self.first_name) > 50:
            raise ValueError("First name is required and must be <= 50 characters")
        if not self.last_name or len(self.last_name) > 50:
            raise ValueError("Last name is required and must be <= 50 characters")
        if not self.email or '@' not in self.email:
            raise ValueError("Valid email is required")
