from flask import url_for
from .test_base import BaseTestCase
from app.models import Tweet, User
from app import db

class UserViewsTests(BaseTestCase):
    def test_posting_tweet(self):
        u = User(username='user1', password='password123', email='user1@gmail.com')
        db.session.add(u)
        db.session.commit()

        with self.client:
            self.client.post(url_for('auth.login'), data={'username': 'user1', 'password':'password123'})
            self.client.post(url_for('main.index'), data={'tweet_text': 'first tweet'})
            self.assertIsNotNone(Tweet.query.filter_by(text='first tweet').first())
            self.assertTrue(Tweet.query.filter_by(text='first tweet').first().author.username == 'user1')




