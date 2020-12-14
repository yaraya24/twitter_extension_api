from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email_address = db.Column(db.String(128), unique=True)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.Date, default=datetime.now())
    url_name = db.Column(db.String(126))
    verified = db.Column(db.Boolean, default=False)
    


    
    tweets = db.relationship('Tweet', backref='author', lazy='dynamic') #dynamic ensures the query isn't executed immediately so we can do shit like get it ordered alphabetically
    retweets = db.relationship('Retweet', backref='author', lazy='dynamic')


    @property
    def password(self):
        raise AttributeError('Password is not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    
    def __repr__(self):
        return f'<User {self.username}>'


class Tweet(db.Model):
    __tablename__ = 'tweets'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    source = db.Column(db.String(128), default='Web')
    text = db.Column(db.String(280), nullable = False)
    language = db.Column(db.String(64), default='English')
    created_at = db.Column(db.DateTime, default=datetime.now())

    retweets = db.relationship('Retweet', backref='original', lazy='dynamic')
    scheduled = db.relationship('ScheduledTweet', backref='tweet', lazy='dynamic')
    hashtags = db.relationship('Hashtag', backref='tweet', lazy='dynamic')


class Retweet(db.Model):
    __tablename__ = 'retweets'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id')) #backref = author
    original_tweet_id = db.Column(db.Integer, db.ForeignKey('tweets.id')) #backref=original
    created_at = db.Column(db.DateTime, default=datetime.now())
    text = db.Column(db.String(280), nullable = True)

class ScheduledTweet(db.Model):
    __tablename__ = "scheduled_tweets"
    id = db.Column(db.Integer, primary_key=True)
    scheduled_time = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    tweet_id = db.Column(db.Integer, db.ForeignKey('tweets.id')) #backref=tweet


class Hashtag(db.Model):
    __tablename__ = "hashtags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    tweet = tweet_id = db.Column(db.Integer, db.ForeignKey('tweets.id')) #backref= tweet
