from flask import url_for
from .test_base import BaseTestCase
from app.models import User
from app import db
from flask_login import current_user

class UserViewsTests(BaseTestCase):

    def test_users_can_login(self):
        u = User(username='user1', password='password123', email='user1@gmail.com')
        db.session.add(u)
        db.session.commit()

        with self.client:
            response = self.client.post(url_for('auth.login'), data={'username': 'user1', 'password':'password123'})
            self.assert_redirects(response, url_for('main.index'))
            self.assertTrue(current_user.username == 'user1')
            self.assertTrue(current_user.is_authenticated)

    def test_users_can_logout(self):
        u = User(username='user1', password='password123', email='user1@gmail.com')
        db.session.add(u)
        db.session.commit()

        with self.client:
            self.client.post(url_for('auth.login'), data={'username': 'user1', 'password':'password123'})
            self.client.get(url_for('auth.logout'))
            self.assertTrue(current_user.is_anonymous)

    def register_users(self):
        with self.client:
            self.client.post(url_for('auth.register'), data={'username': 'user1', 'password':'password123', 'email':"user1@gmail.com"})
            self.assertIsNotNone(User.filter_by(username='user1').first())
            self.assertisNone(User.filter_by(username='user').first())


