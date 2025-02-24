#!/usr/bin/env python3
""" Module de gestion des commodités """
from flask_restx import Namespace, Resource

api_amenity = Namespace('amenities', description="Gestion des commodités")

@api_amenity.route('/')
class AmenityList(Resource):
    def get(self):
        """ Récupérer toutes les commodités """
        return {"message": "Liste des commodités"}

    def post(self):
        """ Ajouter une nouvelle commodité """
        return {"message": "Commodité ajoutée"}, 201

@api_amenity.route('/<string:amenity_id>')
class AmenityResource(Resource):
    def put(self, amenity_id):
        """ Mettre à jour une commodité """
        return {"message": f"Commodite {amenity_id} mise a jour"}
