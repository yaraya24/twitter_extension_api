from .. import marsh
from ..models import User, Tweet, Comment, ScheduledTweet, Hashtag
from marshmallow import fields


class CommentSchema(marsh.SQLAlchemyAutoSchema):
    """Marshmallow Schema for the Comment Model
    in order to serialise the data."""

    class Meta:
        model = Comment

    author = marsh.HyperlinkRelated("api.get_user")
    tweet = marsh.HyperlinkRelated("api.get_tweet")


class TweetSchema(marsh.SQLAlchemyAutoSchema):
    """Marshmallow Schema for the Tweet Model
    in order to serialise the data."""

    class Meta:
        model = Tweet

    author = marsh.HyperlinkRelated(
        "api.get_user"
    )  # Provides the API endpoint for the author
    comments = fields.Nested(
        CommentSchema, many=True
    )  # Returns all the comments in that tweet in JSON


class UserSchema(marsh.SQLAlchemyAutoSchema):
    """Marshmallow Schema for the User Model
    in order to serialise the data."""

    class Meta:
        model = User
        load_only = ["password_hash"] # Excludes the password

    tweets = fields.Nested(
        TweetSchema(only=["created_at", "id", "language", "source", "text"]), many=True
    ) # Returns all the tweets authored by the user


class ScheduledTweetSchema(marsh.SQLAlchemyAutoSchema):
    """Marshmallow Schema for the Scheduled Tweet Model
    in order to serialise the data."""

    class Meta:
        model = ScheduledTweet


class HashtagSchema(marsh.SQLAlchemyAutoSchema):
    """Marshmallow Schema for the Hashtag Model
    in order to serialise the data."""
    class Meta:
        model = Hashtag


user_schema = UserSchema()
users_schema = UserSchema(many=True)

tweet_schema = TweetSchema()
tweets_schema = TweetSchema(many=True)

comment_schema = CommentSchema(many=True)

scheduled_tweet_schema = ScheduledTweetSchema()

hashtag_schema = HashtagSchema()
