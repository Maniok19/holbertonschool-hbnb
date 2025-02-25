from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place

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
    
    # USER METHODS

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

    # AMENITY METHODS

    def create_amenity(self, amenity_data):
        return self.amenity_repo.add(amenity_data)

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        return self.amenity_repo.update(amenity_id, amenity_data)

    # PLACES METHODS

    def create_place(self, place_data):
        amenities = place_data.pop('amenities', [])
        
        # Create and validate place
        place = Place(**place_data)
        place.checking()
        
        # Add amenities back to place
        place.amenities = amenities
        
        # Save place to repository
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)


    def get_all_places(self):
        return self.place_repo.get_all()


    def update_place(self, place_id, place_data):
        return self.place_repo.update(place_id, place_data)
    
    def get_place_by_title(self, title):
        return next(
            (place for place in self.place_repo.get_all() if place.title == title),
            None
        )