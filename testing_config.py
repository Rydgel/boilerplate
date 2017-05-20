from flask_testing import TestCase
from app import create_app, db
import os
import json

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseTestConfig(TestCase):
    default_user = {
        "email": "default@gmail.com",
        "password": "something"
    }

    def create_app(self):
        app = create_app()
        app.config.from_object('config.TestingConfig')
        return app

    def setUp(self):
        self.app = self.create_app().test_client()
        db.create_all()
        # todo
        # res = self.app.post(
        #         "/api/create_user",
        #         data=json.dumps(self.default_user),
        #         content_type='application/json'
        # )

        # self.token = json.loads(res.data.decode("utf-8"))["token"]

    def tearDown(self):
        db.session.remove()
        db.drop_all()
