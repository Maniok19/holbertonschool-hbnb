from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    def __init__(self):
        self.user_repo = SQLAlchemyRepository(User)
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)


    # USER METHODS

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
    
    def get_user_by_id(self, user_id):
        return self.user_repository.get(user_id)

    def get_user_by_email(self, email):
        """Get user by email"""
        return next(
            (user for user in self.user_repo.get_all() if user.email == email),
            None
        )

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = User(**user_data)
        user.checking()
        self.user_repo.update(user_id, user_data)
        return user

    # AMENITY METHODS

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        amenity.checking()
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = Amenity(**amenity_data)
        amenity.checking()
        self.amenity_repo.update(amenity_id, amenity_data)
        return amenity

    # REVIEW METHODS
    def create_review(self, review_data):
        """Create a new review"""
        # Create and validate new user
        review = Review(**review_data)
        review.checking()
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Get all reviews for a specific place"""
        # First check if place exists
        place = self.get_place(place_id)
        if not place:
            return None

        # Return all reviews for this place
        return [
            review for review in self.review_repo.get_all()
            if review.place_id == place_id
        ]

    def update_review(self, review_id, review_data):
        review = Review(**review_data)
        review.checking()
        self.review_repo.update(review_id, review_data)
        return review

    def delete_review(self, review_id):
        return self.review_repo.delete(review_id)

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
        amenities = place_data.pop('amenities', [])

        # Create and validate place
        place = Place(**place_data)
        place.checking()

        # Add amenities back to place
        place.amenities = amenities

        # Save place to repository
        self.place_repo.update(place_id, place_data)
        return place

    def get_place_by_title(self, title):
        return next(
            (place for place in self.place_repo.get_all()
                if place.title == title),
            None
        )
 