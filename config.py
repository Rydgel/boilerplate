import os
import datetime

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    SECRET_KEY = '91096dfe00f6e82b34e170c43accb10c7fdbef02e9a39f6e'
    SECURITY_PASSWORD_SALT = '4hsz%Pb2ZtSn,Bw4heO-u *U:TPY>mPkFU2EoL@B]DZ6sIpoK>m^h8Y^hJXp_?^@'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_POOL_RECYCLE = 10
    DEBUG = True
    # todo switch that to ENV var
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/boilerplate'
    # jwt
    JWT_ALGORITHM = 'HS256'
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=60)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=30)


class TestingConfig(object):
    """Development configuration."""
    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    DEBUG_TB_ENABLED = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False


config = BaseConfig()
test_config = TestingConfig()
