 #!/usr/bin/env python3
""" Modèle de données pour les commodités """

from app.models.base import BaseModel

class Amenity(BaseModel):
    """Classe représentant une commodité"""
    def __init__(self, name):
        super().__init__()
        self.name = name

    def checking(self):
        """Validation des données"""
        if not self.name or len(self.name) > 100:
            raise ValueError("Le nom de la commodité est requis et doit être ≤ 100 caractères")

        return True