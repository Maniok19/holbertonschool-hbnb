#!/usr/bin/env python3
from sqlalchemy.ext.hybrid import hybrid_property

from app import db
from app.models.base import BaseModel


class Amenity(BaseModel):
    """
    Class representing an amenity.
    """

    __tablename__ = 'amenities'

    _name = db.Column(db.String(128), nullable=False, unique=True)

    @hybrid_property
    def name(self):
        """
        Get the amenity name.
        """
        return self._name

    @name.setter
    def name(self, value):
        """
        Set the amenity name.
        """
        if not value:
            raise ValueError('Amenity name cannot be empty.')
        if len(value) > 128:
            raise ValueError('Amenity name length exceeds 128 characters.')
        self._name = value

