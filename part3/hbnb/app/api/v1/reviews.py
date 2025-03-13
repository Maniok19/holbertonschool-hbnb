#!/usr/bin/env python3
from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(
        required=True,
        description='Rating of the place (1-5)'
    ),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})


@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'User or Place not found')
    @api.response(500, 'Internal server error')
    def post(self):
        """Register a new review"""
        try:
            review_data = api.payload

            # Check if user exists
            user = facade.get_user(review_data['user_id'])
            if not user:
                return {'error': 'User not found'}, 404

            # Check if place exists
            place = facade.get_place(review_data['place_id'])
            if not place:
                return {'error': 'Place not found'}, 404
            
            #check if the user and the owner place is not the same
            if user.id == place.owner_id:
                return {'error': 'The user and the owner of the place are the same'}, 400

            #check if the user has already made a review for the place
            reviews = facade.get_reviews_by_place(place.id)
            for review in reviews:
                if review.user_id == user.id:
                    return {'error': 'The user has already made a review for the place'}, 400

            new_review = facade.create_review(review_data)
            return {
                'id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating,
                'user_id': new_review.user_id,
                'place_id': new_review.place_id,
            }, 201

        except (ValueError, KeyError) as e:
            return {"error": str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()

        return [
            {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
            }
            for review in reviews
        ], 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user_id,
            'place_id': review.place_id
        }, 200

    @jwt_required()
    @api.expect(review_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update review details"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        data = api.payload

        # Validate place_id exists
        if 'place_id' in data:
            place = facade.get_place(data['place_id'])
            if not place:
                return {'error': 'Place not found'}, 404

        # Validate user_id exists
        if 'user_id' in data:
            user = facade.get_user(data['user_id'])
            if not user:
                return {'error': 'User not found'}, 404

        # Validate rating
        if 'rating' in data:
            if (not isinstance(data['rating'], int) or
                    data['rating'] < 1 or
                    data['rating'] > 5):
                return {'error': 'Rating must be between 1 and 5'}, 400
            
        #check if the user is the same that made the review
        if 'user_id' in data:
            if data['user_id'] != review.user_id:
                return {'error': 'The user is not the same that made the review'}, 400

        try:
            facade.update_review(review_id, data)
            updated_review = facade.get_review(review_id)
            return {
                'id': updated_review.id,
                'user_id': updated_review.user_id,
                'place_id': updated_review.place_id,
                'text': updated_review.text,
                'rating': updated_review.rating
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @jwt_required()
    @api.response(204, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        
        #check if the user is the same that made the review
        current_user = get_jwt_identity()
        
        facade.delete_review(review_id)
        return {"message": "Review deleted successfully"}, 200


@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        reviews = facade.get_reviews_by_place(place_id)
        if reviews is None:  # Place not found
            return {"error": "Place not found"}, 404

        return [
            {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id
            }
            for review in reviews
        ], 200
