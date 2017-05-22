from .. import db, bcrypt, config
from itsdangerous import URLSafeTimedSerializer, BadSignature, \
    SignatureExpired

user_column = db.Column('user_id', db.Integer(), db.ForeignKey('users.id'))
role_column = db.Column('role_id', db.Integer(), db.ForeignKey('roles.id'))
roles_users = db.Table('roles_users', user_column, role_column)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), nullable=False, index=True)
    registered_on = db.Column(db.TIMESTAMP(timezone=True), nullable=False, index=True)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_at = db.Column(db.TIMESTAMP(timezone=True), nullable=True, index=True)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return f"<User: {self.id} {self.email} {self.roles}>"

    @staticmethod
    def hashed_password(password):
        return bcrypt.generate_password_hash(password).decode('utf-8')

    @staticmethod
    def get_user_with_email_and_password(email, password):
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return None

    @property
    def is_confirmed(self):
        return self.confirmed

    @property
    def is_active(self):
        return self.active and self.is_confirmed

    def has_role(self, role):
        if isinstance(role, str):
            return role in (role.name for role in self.roles)
        else:
            return role in self.roles

    @staticmethod
    def generate_confirmation_token(email):
        serializer = URLSafeTimedSerializer(config['SECRET_KEY'])
        return serializer.dumps(email, salt=config['SECURITY_PASSWORD_SALT'])

    @staticmethod
    def confirm_token_email(token, expiration=3600):
        serializer = URLSafeTimedSerializer(config['SECRET_KEY'])
        try:
            email = serializer.loads(
                token,
                salt=config['SECURITY_PASSWORD_SALT'],
                max_age=expiration
            )
        except (BadSignature, SignatureExpired):
            return False
        return email
