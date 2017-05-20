from functools import wraps
from flask import jsonify, redirect
from flask_jwt_extended import get_jwt_claims


def roles_required(*perms):
    """Decorator which specifies that a user must have all the specified roles.
    Example::
        @app.route('/dashboard')
        @roles_required('admin', 'editor')
        def dashboard():
            return 'Dashboard'
    The current user must have both the `admin` role and `editor` role in order
    to view the page.
    :param perms: The required roles.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            user = get_jwt_claims()
            user_roles = user['roles']
            for perm in perms:
                if perm not in user_roles:
                    return jsonify({'error': True, 'msg': 'forbidden'}),\
                           403
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper


def roles_accepted(*perms):
    """Decorator which specifies that a user must have at least one of the
    specified roles. Example::
        @app.route('/create_post')
        @roles_accepted('editor', 'author')
        def create_post():
            return 'Create Post'
    The current user must have either the `editor` role or `author` role in
    order to view the page.
    :param perms: The possible roles.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            user = get_jwt_claims()
            user_roles = user['roles']
            for perm in perms:
                if perm in user_roles:
                    return fn(*args, **kwargs)
            return jsonify({'error': True, 'msg': 'forbidden'}), 403
        return decorated_view
    return wrapper


def anonymous_user_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        user = get_jwt_claims()
        if user is not None:
            return redirect("/")
        return f(*args, **kwargs)
    return wrapper
