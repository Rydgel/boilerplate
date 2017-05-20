from flask import Blueprint, request, jsonify
from app import db
from flask_jwt_extended import jwt_required, \
     get_jwt_claims
from app.models import User, Role
from app.decorators import roles_required
from app.decorators import email_confirmed
import datetime


user_bp = Blueprint('user_endpoint', __name__)


@user_bp.route('/register', methods=['POST'])
def register():
    email = request.values.get('email', False)
    password = request.values.get('password', False)

    # todo rate limiting ip
    # todo recaptcha

    if not email or not password:
        return jsonify(error=True), 401

    user_role = Role.query.filter_by(name="users").first()
    if user_role is None:
        user_role = Role(name="users", description="Users")

    new_user = User(
        email=email,
        password=User.hashed_password(password),
        active=True,
        confirmed=True,
        registered_on=datetime.datetime.now(),
        confirmed_at=datetime.datetime.now())

    new_user.roles.append(user_role)
    db.session.add(new_user)
    db.session.commit()

    token = User.generate_confirmation_token(email)
    # todo send confirmation email


# todo make redirects on success/failure
@user_bp.route('/confirm/<token>', methods=['GET', 'POST'])
@jwt_required
@roles_required('Users')
def confirm_token(token):
    email = User.confirm_token_email(token)
    if not email:
        return jsonify({
            'error': True,
            'msg': 'The confirmation link is invalid or has expired.'}), 403

    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        return jsonify({
            'error': False,
            'msg': 'Account already confirmed. Please login.'})
    else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        return jsonify({
            'error': False,
            'msg': 'You have confirmed your account. Thanks!'})


@user_bp.route('/', methods=['GET'])
@jwt_required
@email_confirmed
def get_user():
    claim = get_jwt_claims()
    jsonify(claim)
