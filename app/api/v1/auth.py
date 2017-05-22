from flask import Blueprint, request, jsonify
from app import bcrypt, jwt
from flask_jwt_extended import jwt_refresh_token_required, \
    create_access_token, create_refresh_token, get_jwt_identity
from app.models import User


auth_bp = Blueprint('auth_endpoint', __name__)


@jwt.user_claims_loader
def add_claims_to_access_token(user):
    return {
        'id': user.id,
        'email': user.email,
        'roles': list(map(lambda r: r.name, user.roles)),
        'confirmed': user.confirmed
    }


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.email


@auth_bp.route('/login', methods=['POST'])
def login():
    email = request.values.get('email', False)
    password = request.values.get('password', False)

    if not email or not password:
        return jsonify(error=True), 401

    user_db = User.query.filter_by(email=email).first()

    if user_db is None or not user_db.is_active \
            or not bcrypt.check_password_hash(user_db.password, password):
        return jsonify(error=True, msg='Wrong username or password'), 401

    ret = {
        'error': False,
        'access_token': create_access_token(identity=user_db, fresh=True),
        'refresh_token': create_refresh_token(identity=user_db)
    }
    return jsonify(ret)


@auth_bp.route('/fresh-login', methods=['POST'])
def fresh_login():
    email = request.values.get('email', False)
    password = request.values.get('password', False)

    if not email or not password:
        return jsonify(error=True), 401

    user_db = User.query.filter_by(email=email).first()

    if user_db is None or not user_db.is_active \
            or not bcrypt.check_password_hash(user_db.password, password):
        return jsonify(error=True, msg='Wrong username or password'), 401

    ret = {
        'error': False,
        'access_token': create_access_token(identity=user_db, fresh=True),
    }
    return jsonify(ret)


@auth_bp.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    jwt_email = get_jwt_identity()
    user_db = User.query.filter_by(email=jwt_email).first()

    if user_db is None:
        return jsonify(error=True), 401

    ret = {
        'error': False,
        'access_token': create_access_token(identity=user_db, fresh=False)
    }
    return jsonify(ret)
