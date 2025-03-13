#!/usr/bin/env python3
""" Modèle de données pour les commodités """

from app.models.base import BaseModel
from app import db

class Amenity(BaseModel):
    """Classe représentant une commodité"""
    __tablename__ = 'amenities'
    
    name = db.Column(db.String(100), nullable=False)
    
    def __init__(self, name):
        super().__init__()
        self.name = name

    def checking(self):
        """Validation des données"""
        if not self.name or len(self.name) > 100:
            raise ValueError(
                "Le nom de commodité est requis et doit être ≤ 100 caractères"
                )
