from flask_restx import Namespace, Resource, fields
from flask import jsonify
from app.services import facade

api = Namespace('places', description='Place operations')

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(
        required=True,
        description='Latitude of the place'
    ),
    'longitude': fields.Float(
        required=True,
        description='Longitude of the place'
    ),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities IDs"),
    'reviews': fields.List(fields.String, description="List of review IDs")
})


@api.route('/')
class PlaceList(Resource):
    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Get list of all places"""
        places = facade.get_all_places()
        return [{
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner_id': place.owner_id,
            'amenities': place.amenities
        } for place in places], 200

    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Title already registered')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Owner not found')
    def post(self):
        """Register a new place"""
        place_data = api.payload

        try:
            owner = facade.get_user(place_data['owner_id'])
            if not owner:
                return {'error': 'Owner not found'}, 404

            existing_place = facade.get_place_by_title(place_data['title'])
            if existing_place:
                return {'error': 'Title already registered'}, 400

            new_place = facade.create_place(place_data)
            return {
                'id': new_place.id,
                'title': new_place.title,
                'description': new_place.description,
                'price': new_place.price,
                'latitude': new_place.latitude,
                'longitude': new_place.longitude,
                'owner_id': new_place.owner_id,
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

@api.route('/<place_id>/amenities/<amenity_id>')
class PlaceAmenityResource(Resource):
    @api.response(200, "Amenity successfully added to place")
    @api.response(404, "Place or Amenity not found")
    @api.response(400, "Amenity already linked to place")
    def post(self, place_id, amenity_id):
        """Add an amenity to a place"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404

        if amenity_id in place.amenities:
            return {'error': 'Amenity already linked to place'}, 400
        
        place.amenities.append(amenity_id)
        facade.update_place(place_id, {'amenities': place.amenities})

        return {"message": "Amenity successfully added to place"}, 200