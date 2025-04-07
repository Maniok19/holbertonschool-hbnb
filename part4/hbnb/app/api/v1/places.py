from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services import facade


api = Namespace('places', description='Place operations')

amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(
        description='Amenity ID'
        ),
    'name': fields.String(
        description='Name of the amenity'
        )
})

user_model = api.model('PlaceUser', {
    'id': fields.String(
        description='User ID'
        ),
    'first_name': fields.String(
        description='First name of the owner'
        ),
    'last_name': fields.String(
        description='Last name of the owner'
        ),
    'email': fields.String(
        description='Email of the owner'
        )
})

review_model = api.model('PlaceReview', {
    'id': fields.String(
        description='Review ID'
        ),
    'text': fields.String(
        description='Text of the review'
        ),
    'rating': fields.Integer(
        description='Rating of the place (1-5)'
        ),
    'user_id': fields.String(
        description='ID of the user'
        )
})

place_model = api.model('Place', {
    'title': fields.String(
        required=True,
        description='Title of the place'
        ),
    'description': fields.String(
        description='Description of the place'
        ),
    'price': fields.Float(
        required=True,
        description='Price per night'
        ),
    'latitude': fields.Float(
        required=True,
        description='Latitude of the place'
        ),
    'longitude': fields.Float(
        required=True,
        description='Longitude of the place'
        ),
    'owner_id': fields.String(
        required=True,
        description='ID of the owner'
        ),
    'amenities': fields.List(
        fields.Nested(amenity_model),
        description='List of amenities'
        ),
    'reviews': fields.List(
        fields.Nested(review_model),
        description='List of reviews'
        )
})


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def post(self):
        """Register a new place"""
        current_user = get_jwt_identity()
        place_data = api.payload
        user = facade.get_user(place_data.get('owner_id'))
        if user is None:
            return {'error': 'Invalid owner_id.'}, 400

        if current_user['id'] != user.id:
            return {'error': 'Unauthorized action.'}, 403
        
        #if place title already exists

        if facade.get_places_by_title(place_data.get('title')):
            return {'error': 'Place title already exists.'}, 400

        amenity_list = []
        if place_data.get('amenities'):
            for amenity in place_data.get('amenities'):
                if facade.get_amenity(amenity['id']) is None:
                    return {'error': 'Invalid amenity ID.'}, 400

        try:
            place = facade.create_place(place_data)
            return {
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': str(place.price),
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner_id': place.owner_id,
                }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = []
        for place in facade.get_all_places():
            places.append({
                'id': place.id,
                'price': str(place.price),
                'description': place.description,
                'title': place.title,
                'latitude': place.latitude,
                'longitude': place.longitude
                })
        return places, 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if place:
            owner = facade.get_user(place.owner_id)
            return {
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': str(place.price),
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner': {
                    'id': owner.id,
                    'first_name': owner.first_name,
                    'last_name': owner.last_name,
                    'email': owner.email,
                    'created_at': str(owner.created_at),
                },
                'amenities': [
                    {
                        'id': amenity.id,
                        'name': amenity.name
                    } for amenity in place.amenities
                ]
            }, 200
        return {'error': 'Place not found.'}, 404

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, place_id):
        """Update a place's information"""
        current_user = get_jwt_identity()
        place_data = api.payload
        
        # Check if place exists
        place = facade.get_place(place_id)
        if place is None:
            return {'error': 'Place not found.'}, 404
            
        # Check user permissions
        if current_user.get('is_admin') is True:
            is_admin = facade.get_user(current_user['id']).is_admin
            if is_admin:
                # Admin can update any place
                pass
            else:
                return {'error': 'Admin privileges required.'}, 403
        else:
            # Regular user can only update their own places
            if current_user['id'] != place.owner_id:
                return {'error': 'Unauthorized action.'}, 403

        # Validate amenities if provided
        if place_data.get('amenities'):
            for amenity in place_data.get('amenities'):
                if facade.get_amenity(amenity['id']) is None:
                    return {'error': 'Invalid amenity ID.'}, 400

        try:
            facade.update_place(place_id, place_data)
        except ValueError as e:
            return {'error': str(e)}, 400
        
        return {'message': 'Place updated successfully.'}, 200

    @api.response(200, 'Place successfully deleted')
    @api.response(404, 'Place not found')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def delete(self, place_id):
        """Delete a place"""
        current_user = get_jwt_identity()
        user = facade.get_user(current_user['id'])
        
        place = facade.get_place(place_id)
        if place is None:
            return {'error': 'Place not found.'}, 404
            
        # Allow deletion if user is admin or the owner of the place
        is_admin = user.is_admin if hasattr(user, 'is_admin') else False
        is_owner = current_user['id'] == place.owner_id
        
        if not (is_admin or is_owner):
            return {'error': 'Unauthorized action.'}, 403

        facade.delete_place(place_id)
        return {'message': 'Place successfully deleted.'}, 200

@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get reviews for a place"""
        place = facade.get_place(place_id)
        if place:
            reviews = []
            for review in place.reviews:
                reviews.append({
                    'id': review.id,
                    'text': review.text,
                    'rating': review.rating,
                    'user_id': review.user_id
                })
            return reviews, 200
        return {'error': 'Place not found.'}, 404
