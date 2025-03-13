from flask import Flask
from flask_restx import Api

# Import extensions from the new module
from app.extensions import db, bcrypt, jwt

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions with app
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    # Import models and routes after extensions are defined
    from app.models import base, user, place, amenity, review
    
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API',
              security='Bearer Auth', authorizations={
                  'Bearer Auth': {
                      'type': 'apiKey',
                      'in': 'header',
                      'name': 'Authorization',
                      'description': "Jwt authorization header"
                  }
              })

    from app.api.v1.users import api as users_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.places import api as place_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.auth import api as auth_ns
    from app.api.v1.protected import api as protected_ns
    # Register the users namespace
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(place_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(protected_ns, path='/api/v1/protected')
    
    return app
