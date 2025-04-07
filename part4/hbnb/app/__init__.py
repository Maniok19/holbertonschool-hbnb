from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy 
from app.extensions import db, bcrypt, jwt

jwt = JWTManager()
bcrypt = Bcrypt()

# Import all your namespaces
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as place_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns
from app.api.v1.protected import api as protected_ns
     
def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Update CORS configuration to support credentials
    CORS(app, resources={r"/api/*": {"origins": ["http://localhost:5500", "http://127.0.0.1:5500"], 
                                     "supports_credentials": True}})
    
    @app.route('/api/v1/places', methods=['OPTIONS'])
    def handle_options():
        return '', 200

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    # Create the API
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API',
              security='Bearer Auth', authorizations={
                  'Bearer Auth': {
                      'type': 'apiKey',
                      'in': 'header',
                      'name': 'Authorization',
                      'description': "Jwt authorization header"
                  }
              })
              
    # Register the namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(place_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(protected_ns, path='/api/v1/protected')

    # Create tables
    with app.app_context():
        db.create_all()
        
    return app