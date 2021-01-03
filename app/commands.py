from . import db
from flask import Blueprint

db_commands = Blueprint("db_commands", __name__)


@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    db.engine.execute("DROP TABLE IF EXISTS alembic_version;")
    print("Tables deleted")


@db_commands.cli.command("seed")
def seed_db():
    from .models import User, Tweet, ScheduledTweet, Comment, Hashtag, Follow
    from faker import Faker
    from random import choice
    from sqlalchemy.exc import IntegrityError

    Users = []
    Tweets = []

    def users(count=20):
        fake = Faker()
        i = 0
        while i < count:
            u = User(
                email=fake.email(),
                username=fake.user_name(),
                password="password123",
                created_at=fake.past_date(),
            )
            db.session.add(u)
            try:
                db.session.commit()
                Users.append(u)
                i += 1
            except IntegrityError:
                db.session.rollback()

    def tweets(count=50):
        fake = Faker()
        for i in range(count):
            u = choice(Users)
            t = Tweet(text=fake.text(), author=u, created_at=fake.past_date())
            db.session.add(t)
            Tweets.append(t)
        db.session.commit()

    def comments(count=100):
        fake = Faker()
        for i in range(count):
            u = choice(Users)
            t = choice(Tweets)
            c = Comment(
                body=fake.text(), author=u, tweet=t, created_at=fake.past_date()
            )
            db.session.add(c)
        db.session.commit()

    def hashtags(count=200):
        hashtag_values = [
            "Love",
            "Instagood",
            "Fashion",
            "tbt",
            "cute",
            "followme",
            "selfie",
            "friends",
            "family",
            "summer",
            "fun",
            "art",
            "nature",
            "smile",
        ]
        for i in range(count):
            t = choice(Tweets)
            h = Hashtag(name=choice(hashtag_values), tweet=t)
            db.session.add(h)
        db.session.commit()

    def follows(count=20):
        i = 0
        while i < count:
            follower = choice(Users)
            followed = choice(Users)
            if follower == followed or follower.is_following(followed):
                continue
            f = Follow(follower=follower, followed=followed)
            db.session.add(f)
            i += 1
        db.session.commit()

    users()
    tweets()
    comments()
    hashtags()
    follows()
    print("Tables Seeded")
