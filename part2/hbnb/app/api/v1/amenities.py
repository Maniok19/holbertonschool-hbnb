#!/usr/bin/env python3
""" Module de gestion des commodités """
from flask_restx import Namespace, Resource, fields
from app.models.amenity import Amenity
from app.services import facade
from app.services import HBnBFacade


api_amenity = Namespace('amenities', description="Gestion des commodités")

amenity_model = api_amenity.model('Amenity', {
    'name': fields.String(required=True, description="Nom de la commodité")
})

@api_amenity.route('/')
class AmenityList(Resource):
    def get(self):
        """ Récupérer toutes les commodités """
        amenities = facade.get_all_amenities()
        return [amenity.to_dict() for amenity in amenities]

    @api_amenity.expect(amenity_model, validate=True)
    def post(self):
        """ Ajouter une nouvelle commodité """
        data = api_amenity.payload
        try:
            new_amenity = Amenity(name=data['name'])
            new_amenity.validate()
            facade.save_amenity(new_amenity)
            return {
                 "id": str(new_amenity.id),
                "name": new_amenity.name
            }, 201
        except ValueError as e:
            return {"error": str(e)}, 400

@api_amenity.route('/<string:amenity_id>')
class AmenityResource(Resource):
    def put(self, amenity_id):
        """ Mettre à jour une commodité """
        data = api_amenity.payload
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Commodité non trouvée"}, 404
        
        if "name" in data:
            amenity.name = data["name"]
        
        facade.save_amenity(amenity)
        return {"message": f"Commodité {amenity_id} mise à jour"}
