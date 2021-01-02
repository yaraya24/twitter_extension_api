from .. import marsh
from ..models import User, Tweet, Comment, ScheduledTweet, Hashtag
from marshmallow import fields
from marshmallow.validate import Length

    
class CommentSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = Comment

    author = marsh.HyperlinkRelated("api.get_user")
    tweet = marsh.HyperlinkRelated("api.get_tweet")


class TweetSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = Tweet

    author = marsh.HyperlinkRelated("api.get_user")
    comments = fields.Nested(CommentSchema, many=True)


class UserSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_only = ["password_hash"]
    
    tweets = fields.Nested(TweetSchema(only = ["created_at", "id", "language", "source", "text"]), many=True)
    


class ScheduledTweetSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = ScheduledTweet


class HashtagSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = Hashtag

user_schema = UserSchema()
users_schema = UserSchema(many=True)

tweet_schema = TweetSchema()
tweets_schema = TweetSchema(many=True)

comment_schema = CommentSchema(many=True)

scheduled_tweet_schema = ScheduledTweetSchema()

hashtag_schema = HashtagSchema()
