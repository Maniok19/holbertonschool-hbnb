from sqlalchemy.ext.hybrid import hybrid_property

from app import db
from app.models.base import BaseModel

class Place(BaseModel):
    """Class representing a place/property"""
    __tablename__ = 'places'
    
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    owner = db.relationship('User', backref='places')
    amenities = db.relationship(
        'Amenity',
        secondary='place_amenity',
        back_populates='places',
        collection_class=list
    )
    
    def __init__(self, title, description, price, latitude=None, longitude=None, owner_id=None, amenities=None):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.amenities = amenities or []
    
    def checking(self):
        """Validate place data"""
        if not self.title or len(self.title) > 100:
            raise ValueError("Title is required and must be ≤ 100 characters")
        if self.price <= 0:
            raise ValueError("Price must be greater than 0")