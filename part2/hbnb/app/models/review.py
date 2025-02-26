 #!/usr/bin/env python3

from app.models.base import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    def checking(self):
        # Vérification du texte
        if self.text is None or not isinstance(self.text, str):
            raise ValueError("Le texte doit être une chaîne de caractères.")
        
        if self.rating is None or not (0 <= self.rating <= 5):
            raise ValueError("La note doit être un nombre entier entre 0 et 5.")
        
        if self.place is None or not isinstance(self.place, str):
            raise ValueError("Le lieu doit être une chaîne de caractères.")
        
        if self.user is None or not isinstance(self.user, str):
            raise ValueError("L'utilisateur doit être une chaîne de caractères.")
        
        return True