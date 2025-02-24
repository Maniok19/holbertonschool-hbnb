from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns

# Debugging import for amenities
try:
    from app.api.v1.amenities import api as api_amenity
    print("Successfully imported api from amenities")
except ImportError as e:
    print(f"Error importing api from amenities: {e}")

def create_app():
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')

    # Register the users namespace
    api.add_namespace(users_ns, path='/api/v1/users')

    # Register the amenities namespace
    try:
        api.add_namespace(api_amenity, path="/api/v1/amenities")
    except NameError as e:
        print(f"Error adding namespace for amenities: {e}")

    return app
