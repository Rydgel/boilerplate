from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
admin_manager = Admin()


def create_app():
    # Create a flask app
    app = Flask(__name__)

    # Load config into app
    app.config.from_object(config)

    db.init_app(app)
    from . import models
    bcrypt.init_app(app)
    jwt.init_app(app)

    # back-office
    admin_manager.template_mode = "bootstrap3"
    admin_manager.init_app(app)

    from .admin.user_admin import UserAdmin
    admin_manager.add_view(UserAdmin(models.User, db.session))
    admin_manager.add_view(ModelView(models.Role, db.session))

    # API endpoints
    from app.api.global_handlers import global_handlers
    global_handlers(app)
    from app.api.v1.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix=r'/v1/auth')

    from app.api.v1.user import user_bp
    app.register_blueprint(user_bp, url_prefix=r'/v1/user')

    return app
