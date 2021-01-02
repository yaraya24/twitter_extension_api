import unittest
from flask import current_app
from flask_testing import TestCase
from app import create_app, db

class BaseTestCase(TestCase):

    def create_app(self):
        app = create_app('testing')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
         db.session.remove()
         db.drop_all()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

    