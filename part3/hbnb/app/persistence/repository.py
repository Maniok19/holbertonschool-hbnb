from abc import ABC, abstractmethod
from app import db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity



class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class InMemoryRepository(Repository):
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        self._storage[obj.id] = obj

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        return next(
            (obj for obj in self._storage.values()
             if getattr(obj, attr_name) == attr_value),
            None
        )

class PlaceRepository:
    @staticmethod
    def create(place_data):
        place = Place(**place_data)
        db.session.add(place)
        db.session.commit()
        return place

    @staticmethod
    def get(place_id):
        return Place.query.get(place_id)

    @staticmethod
    def get_all():
        return Place.query.all()

    @staticmethod
    def update(place_id, place_data):
        Place.query.filter_by(id=place_id).update(place_data)
        db.session.commit()

    @staticmethod
    def delete(place_id):
        place = Place.query.get(place_id)
        db.session.delete(place)
        db.session.commit()

class ReviewRepository:
    @staticmethod
    def create(review_data):
        review = Review(**review_data)
        db.session.add(review)
        db.session.commit()
        return review

    @staticmethod
    def get(review_id):
        return Review.query.get(review_id)

    @staticmethod
    def get_all():
        return Review.query.all()

    @staticmethod
    def update(review_id, review_data):
        Review.query.filter_by(id=review_id).update(review_data)
        db.session.commit()

    @staticmethod
    def delete(review_id):
        review = Review.query.get(review_id)
        db.session.delete(review)
        db.session.commit()

class AmenityRepository:
    @staticmethod
    def create(amenity_data):
        amenity = Amenity(**amenity_data)
        db.session.add(amenity)
        db.session.commit()
        return amenity

    @staticmethod
    def get(amenity_id):
        return Amenity.query.get(amenity_id)

    @staticmethod
    def get_all():
        return Amenity.query.all()

    @staticmethod
    def update(amenity_id, amenity_data):
        Amenity.query.filter_by(id=amenity_id).update(amenity_data)
        db.session.commit()

    @staticmethod
    def delete(amenity_id):
        amenity = Amenity.query.get(amenity_id)
        db.session.delete(amenity)
        db.session.commit()

class SQLAlchemyRepository(Repository):
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        return self.model.query.get(obj_id)

    def get_all(self):
        return self.model.query.all()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        return self.model.query.filter_by(**{attr_name: attr_value}).first()

class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email):
        return self.model.query.filter_by(email=email).first()

    def add(self, obj):
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        return self.model.query.get(obj_id)

    def get_all(self):
        return self.model.query.all()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        return self.model.query.filter_by(**{attr_name: attr_value}).first()