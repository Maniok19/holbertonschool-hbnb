from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.models.amenity import Amenity

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

    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        data = api.payload
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



@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Commodité non trouvée"}, 404
        return amenity.to_dict(), 200
    
    @api.expect(amenity_model)
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
        
        facade.save_amenity(amenity)
        return {"message": f"Commodité {amenity_id} mise à jour"}
