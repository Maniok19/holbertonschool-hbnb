#!/usr/bin/env python3
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""

        
        review_data = api.payload
            # Check for existing user
        existing_user = facade.get_user(review_data)
        if existing_user:
            return {'error': 'Email already registered'}, 400
        try:
            new_review = facade.create_review(review_data)

            return {
                'id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating,
                'user_id': new_review.user_id,
                'place_id': new_review.place_id
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

@api.expect(review_model)
@api.response(200, 'Review updated successfully')
@api.response(404, 'Review not found')
@api.response(400, 'Invalid input data')
def put(self, review_id):
    """Update a review's information"""
    review = facade.get_review(review_id)
    if not review:
        return {"error": "Review not found"}, 404

    review_data = api.payload
    try:
        updated_review = facade.update_review(review_id, review_data)
        return {
            'id': updated_review.id,
            'text': updated_review.text,
            'rating': updated_review.rating,
        }, 200
    except (ValueError, KeyError) as e:
        return {"error": str(e)}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        facade.delete_review(review_id)
        return {"message": "Review deleted successfully"}, 200
    

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        reviews = facade.get_reviews_by_place(place_id)
        if not reviews:
            return {"error": "Place not found"}, 404
        return [
            {
                'id': review.id,
                'text': review.text,
            }
            for review in reviews
        ], 200