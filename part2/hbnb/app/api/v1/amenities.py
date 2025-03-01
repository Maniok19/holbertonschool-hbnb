from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return [
            {
                "id": amenity.id,
                "name": amenity.name
            }
            for amenity in amenities
        ], 200

    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        
        try:
            amenity_data = api.payload
            new_amenity = facade.create_amenity(amenity_data)
            
            return {
                "id": new_amenity.id,
                "name": new_amenity.name
            }, 201
        except (ValueError, KeyError) as e:
            return {"error": str(e)}, 400


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Commodité non trouvée"}, 404
        return {
                "id": amenity.id,
                "name": amenity.name
            }, 200

    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        data = api.payload
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Commodité non trouvée"}, 404

        if "name" in data:
            amenity.name = data["name"]
        else:
            return {"error": "Données invalides"}, 400

        facade.update_amenity(amenity, data)
        return {"message": "Amenity updated successfully"}, 200
