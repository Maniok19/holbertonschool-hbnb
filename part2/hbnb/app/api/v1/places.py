from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities IDs")
})

@api.route('/')
class PlaceList(Resource):
    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Get list of all places"""
        places = facade.get_all_places()
        return [
            {
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner_id': place.owner_id,
                'amenities': place.amenities
            }
            for place in places
        ], 200

    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Title already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        place_data = api.payload

        try:
            # Check for existing place with the same title
            existing_place = facade.get_place_by_title(place_data['title'])
            if existing_place:
                return {'error': 'Title already registered'}, 400

            # Create new place if title is unique
            new_place = facade.create_place(place_data)

            return {
                'id': new_place.id,
                'title': new_place.title,
                'description': new_place.description,
                'price': new_place.price,
                'latitude': new_place.latitude,
                'longitude': new_place.longitude,
                'owner_id': new_place.owner_id,
                'amenities': new_place.amenities
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner_id': place.owner_id,
            'amenities': place.amenities
        }, 200

    @api.expect(place_model, validate=True)
    @api.response(200, 'Place successfully updated')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update place details"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        update_data = api.payload

        # Check if title is being changed and is already taken
        if update_data.get('title') != place.title:
            existing_place = facade.get_place_by_title(update_data['title'])
            if existing_place:
                return {'error': 'Title already registered'}, 400

        try:
            facade.update_place(place_id, update_data)
            place = facade.get_place(place_id)  # Get updated place
            return {
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner_id': place.owner_id,
                'amenities': place.amenities
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400