from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_claims


def email_confirmed(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        user = get_jwt_claims()
        if not user.confirmed:
            return jsonify({'error': True, 'msg': 'Email not confirmed'})
        return f(*args, **kwargs)
    return wrapper
