from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager

class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    started_following = db.Column(db.DateTime, default=datetime.utcnow)


class User(UserMixin, db.Model):

    def username_default(context):
        url_name = context.get_current_parameters()['username']
        return f'www.twitter.com/{url_name}'

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(128), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.Date, default=datetime.utcnow)
    url_name = db.Column(db.String(128), default=username_default)
    verified = db.Column(db.Boolean, default=False)
           
    tweets = db.relationship('Tweet', backref='author', lazy='dynamic') #dynamic ensures the query isn't executed immediately so we can do shit like get it ordered alphabetically
    comments = db.relationship('Comment', backref='author', lazy='dynamic')

    following = db.relationship('Follow', 
                                foreign_keys=[Follow.follower_id],
                                backref=db.backref('follower', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')

    followers = db.relationship('Follow',
                                foreign_keys=[Follow.followed_id],
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')




    @property
    def password(self):
        raise AttributeError('Password is not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_following(self, user):
        if user.id is None:
            return False
        return self.following.filter_by(followed_id=user.id).first() is not None

    def is_followed_by(self, user):
        if user.id is None:
            return False
        return self.followers.filter_by(follower_id=user.id).first() is not None

    def follow(self, user):
        if not self.is_following(user):
            f = Follow(follower=self, followed=user)
            db.session.add(f)

    def unfollow(self, user):
        f = self.following.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Tweet(db.Model):
    __tablename__ = 'tweets'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    source = db.Column(db.String(128), default='Web')
    text = db.Column(db.String(280), nullable = False)
    language = db.Column(db.String(64), default='English')
    created_at = db.Column(db.DateTime, default=datetime.now)

    retweets = db.relationship('Retweet', backref='original', lazy='dynamic')
    scheduled = db.relationship('ScheduledTweet', backref='tweet', lazy='dynamic')
    hashtags = db.relationship('Hashtag', backref='tweet', lazy='dynamic', cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='tweet', lazy='dynamic', cascade='all, delete-orphan')


class Retweet(db.Model):
    __tablename__ = 'retweets'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id')) #backref = author
    original_tweet_id = db.Column(db.Integer, db.ForeignKey('tweets.id')) #backref=original
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    text = db.Column(db.String(280), nullable = True)

class ScheduledTweet(db.Model):
    __tablename__ = "scheduled_tweets"
    id = db.Column(db.Integer, primary_key=True)
    scheduled_time = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tweet_id = db.Column(db.Integer, db.ForeignKey('tweets.id')) #backref=tweet


class Hashtag(db.Model):
    __tablename__ = "hashtags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    tweet_id =  db.Column(db.Integer, db.ForeignKey('tweets.id')) #backref= tweet

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id')) #backref = author
    post_id = db.Column(db.Integer, db.ForeignKey('tweets.id')) #backref = tweet

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))