from flask_restx import Namespace, Resource, fields
from app.services import facade
import re

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(
        required=True,
        description='First name of the user'
    ),
    'last_name': fields.String(
        required=True,
        description='Last name of the user'
    ),
    'email': fields.String(required=True, description='Email of the user')
})


@api.route('/')
class UserList(Resource):
    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Get list of all users"""
        users = facade.get_all_users()
        return [
            {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }
            for user in users
        ], 200

    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        try:
            # Check for existing user with same email
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user:
                return {'error': 'Email already registered'}, 400

            # Create new user if email not found
            new_user = facade.create_user(user_data)

            # Return user data including ID in the response
            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email
            }, 201

        except ValueError as e:
            return {'error': str(e)}, 400


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
            }, 200

    @api.expect(user_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """Update user details"""
        # Get the user first
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        # Get updated data from request
        update_data = api.payload

        # Validate email format if email is being updated
        if 'email' in update_data:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, update_data['email']):
                return {'error': 'Invalid email format'}, 400

        # Check if email is being changed and is already taken
        if 'email' in update_data and update_data.get('email') != user.email:
            existing_user = facade.get_user_by_email(update_data['email'])
            if existing_user:
                return {'error': 'Email already registered'}, 400
            # Validate that email is not empty
        if 'email' in update_data and not update_data['email']:
            return {'error': 'Email cannot be empty'}, 400

        # Validate that first_name is not empty
        if 'first_name' in update_data and not update_data['first_name']:
            return {'error': 'First name cannot be empty'}, 400

        # Validate that last_name is not empty
        if 'last_name' in update_data and not update_data['last_name']:
            return {'error': 'Last name cannot be empty'}, 400

        # Update user
        try:
            facade.update_user(user_id, update_data)
            user = facade.get_user(user_id)  # Get updated user
            return {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400
