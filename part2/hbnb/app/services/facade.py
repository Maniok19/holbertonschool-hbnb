from app.persistence.repository import InMemoryRepository
from app.models.user import User

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        """
        Create a new user after checking for duplicate email
        Raises ValueError if email already exists
        """
        # Check for duplicate email before creating user
        existing_user = self.get_user_by_email(user_data['email'])
        if existing_user:
            raise ValueError("Email already registered")
        
        # Create and validate new user
        user = User(**user_data)
        user.checking()
        self.user_repo.add(user)
        return user
    
    def get_user(self, user_id):
        return self.user_repo.get(user_id)
    
    def get_user_by_email(self, email):
        """Get user by email"""
        return next(
            (user for user in self.user_repo.get_all() if user.email == email),
            None
        )

    def get_all_users(self):
        return self.user_repo.get_all()
    
    def update_user(self, user_id, user_data):
        user = self.get_user(user_id)
        if user:
            self.user_repo.update(user_id, user_data)
