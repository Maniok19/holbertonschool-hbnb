from app.models.base import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place_id, user_id):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place_id = place_id  # Changed from place to place_id
        self.user_id = user_id    # Changed from user to user_id

    def checking(self):
        # Vérification du texte
        if self.text is None or not isinstance(self.text, str):
            raise ValueError("Le texte doit être une chaîne de caractères.")
        
        if self.rating is None or not (0 < self.rating <= 5):
            raise ValueError("La note doit être un nombre entier entre 0 et 5.")
        
        if self.place_id is None or not isinstance(self.place_id, str):
            raise ValueError("Le lieu doit être une chaîne de caractères.")
        
        if self.user_id is None or not isinstance(self.user_id, str):
            raise ValueError("L'utilisateur doit être une chaîne de caractères.")
        
        return True