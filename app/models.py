from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager


class Follow(db.Model):
    """Model that creates a self-referential many-to-many relationship
    for users who follow one another.
    """

    __tablename__ = "follows"
    follower_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    started_following = db.Column(db.DateTime, default=datetime.utcnow)


class User(UserMixin, db.Model):
    """ ORM Model that represents the user"""

    def username_default(context):
        """Helper function to create a default URL value based on the
        username.
        """

        url_name = context.get_current_parameters()["username"]
        return f"www.twitter.com/{url_name}"

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(128), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.Date, default=datetime.utcnow)
    url_name = db.Column(db.String(128), default=username_default)
    verified = db.Column(db.Boolean, default=False)

    tweets = db.relationship(
        "Tweet",
        backref="author",
        lazy="dynamic",  # Lazy='dynamic' to allow queries to be filtered
    )
    comments = db.relationship("Comment", backref="author", lazy="dynamic")

    following = db.relationship(
        "Follow",
        foreign_keys=[Follow.follower_id],
        backref=db.backref("follower", lazy="joined"),
        lazy="dynamic",
        cascade="all, delete-orphan",  # Ensures that if a user is removed, the the relationship is also deleted
    )

    followers = db.relationship(
        "Follow",
        foreign_keys=[Follow.followed_id],
        backref=db.backref("followed", lazy="joined"),
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    @property
    def password(self):
        """ Property function to ensure the password cannot be accessed"""
        raise AttributeError("Password is not readable")

    @password.setter
    def password(self, password):
        """ Setter from the property decorator to hash the password upon creating it"""
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """ Function that will verify the password provided and the hash"""
        return check_password_hash(self.password_hash, password)

    def is_following(self, user):
        """ Function to check if a user is following another user"""
        if user.id is None:
            return False
        return self.following.filter_by(followed_id=user.id).first() is not None

    def is_followed_by(self, user):
        """ Function to check if a user is being followed by another user"""
        if user.id is None:
            return False
        return self.followers.filter_by(follower_id=user.id).first() is not None

    def follow(self, user):
        """Function to create an entry in the follow table to represent a user
        following another user
        """
        if not self.is_following(user):
            f = Follow(follower=self, followed=user)
            db.session.add(f)

    def unfollow(self, user):
        """Function to delete an entry in the follow table to represent
        unfollowing a user"""
        f = self.following.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)

    def __repr__(self):
        return f"<User {self.username}>"


class Tweet(db.Model):
    """ ORM model representing a tweet """

    __tablename__ = "tweets"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    source = db.Column(db.String(128), default="Web")
    text = db.Column(db.String(280), nullable=False)
    language = db.Column(db.String(64), default="English")
    created_at = db.Column(db.DateTime, default=datetime.now)

    scheduled = db.relationship(
        "ScheduledTweet", backref="tweet", lazy="dynamic", cascade="all, delete-orphan"
    )
    hashtags = db.relationship(
        "Hashtag", backref="tweet", lazy="dynamic", cascade="all, delete-orphan"
    )
    comments = db.relationship(
        "Comment", backref="tweet", lazy="dynamic", cascade="all, delete-orphan"
    )


class ScheduledTweet(db.Model):
    """ ORM model representing a scheduled tweet"""

    __tablename__ = "scheduled_tweets"
    id = db.Column(db.Integer, primary_key=True)
    scheduled_time = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tweet_id = db.Column(db.Integer, db.ForeignKey("tweets.id"))


class Hashtag(db.Model):
    """ ORM model representing hashtags within a tweet"""

    __tablename__ = "hashtags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    tweet_id = db.Column(db.Integer, db.ForeignKey("tweets.id"))


class Comment(db.Model):
    """ ORM model representing comments for a tweet"""

    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("tweets.id"))


@login_manager.user_loader
def load_user(user_id):
    """Function used by Flask Login to retrieve information on
    the user.
    """
    return User.query.get(int(user_id))