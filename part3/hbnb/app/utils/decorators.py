from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import jsonify

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user = get_jwt_identity()
        if not current_user or not current_user.get('is_admin'):
            return jsonify({"message": "Accès refusé. Privilèges d'administrateur requis."}), 403
        return f(*args, **kwargs)
    return decorated_function