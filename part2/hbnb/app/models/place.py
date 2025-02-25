from app.models.base import BaseModel

class Place(BaseModel):
    def __init__(self, price, latitude, longitude, description, owner, title):
        super().__init__()
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.description = description
        self.owner = owner
        self.title = title

    def checking(self):
        # Vérification du prix
        if self.price is None or self.price < 0:
            raise ValueError("Le prix doit être un nombre positif.")

        # Vérification de la latitude
        if self.latitude is None or not (-90 <= self.latitude <= 90):
            raise ValueError("La latitude doit être comprise entre -90 et 90.")

        # Vérification de la longitude
        if self.longitude is None or not (-180 <= self.longitude <= 180):
            raise ValueError("La longitude doit être comprise entre -180 et 180.")

        # Vérification de la description
        if not isinstance(self.description, str) or len(self.description) < 10:
            raise ValueError("La description doit être une chaîne de caractères d'au moins 10 caractères.")

        # Vérification du propriétaire (owner)
        if not isinstance(self.owner, str) or len(self.owner.strip()) == 0:
            raise ValueError("L'owner doit être une chaîne de caractères non vide.")

        # Vérification du titre
        if not isinstance(self.title, str) or len(self.title.strip()) < 3:
            raise ValueError("Le titre doit être une chaîne de caractères d'au moins 3 caractères.")

        return True  # Si toutes les vérifications passent, retourne True