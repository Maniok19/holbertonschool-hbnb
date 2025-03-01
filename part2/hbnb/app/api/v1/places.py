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
    'amenities': fields.List(
        fields.String,
        required=True,
        description="List of amenities IDs"
    )
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
    @api.response(404, 'Owner not found')
    def post(self):
        """Register a new place"""
        place_data = api.payload

        try:
            # First check if the owner exists
            owner = facade.get_user(place_data['owner_id'])
            if not owner:
                return {'error': 'Owner not found'}, 404

            # Check for existing place with same title
            existing_place = facade.get_place_by_title(place_data['title'])
            if existing_place:
                return {'error': 'Title already registered'}, 400

            # Ervything is fine, create the place
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


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        owner = facade.get_user(place.owner_id)
        owner_data = {
            'id': owner.id,
            'first_name': owner.first_name,
            'last_name': owner.last_name,
            'email': owner.email
        } if owner else None

        # Get all amenities for the place
        amenity_data = []
        for amenity_id in place.amenities:
            amenity = facade.get_amenity(amenity_id)
            if amenity:
                amenity_data.append({
                    'id': amenity.id,
                    'name': amenity.name
                })

        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': owner_data,
            'amenities': amenity_data
        }, 200

    @api.expect(place_model, validate=True)
    # Changed to validate=False to allow partial updates
    @api.response(200, 'Place successfully updated')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update place details"""
        # Get the place first
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        # Get updated data from request
        update_data = api.payload

        # Check if owner exists
        owner = facade.get_user(update_data['owner_id'])
        if not owner:
            return {'error': 'Owner not found'}, 404
        #check for title exist
        existing_place = facade.get_place_by_title(update_data['title'])
        if existing_place:
            return {'error': 'Title already registered'}, 400
        # Update place
        try:
            facade.update_place(place_id, update_data)
            updated_place = facade.get_place(place_id)
            return {
                'id': updated_place.id,
                'title': updated_place.title,
                'description': updated_place.description,
                'price': updated_place.price,
                'latitude': updated_place.latitude,
                'longitude': updated_place.longitude,
                'owner_id': updated_place.owner_id,
                'amenities': updated_place.amenities
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400


@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        reviews = facade.get_reviews_by_place(place_id)
        if reviews is None:  # Place not found
            return {"error": "Place not found"}, 404

        # Return empty list if no reviews, but place exists
        return [
            {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id
            }
            for review in reviews
        ], 200
