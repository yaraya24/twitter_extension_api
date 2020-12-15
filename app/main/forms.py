from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, Regexp


class PostTweet(FlaskForm):
    tweet_text = TextAreaField("What you thinking?", validators=[DataRequired()])
    submit = SubmitField('Post')