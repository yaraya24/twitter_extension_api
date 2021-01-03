from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    TextAreaField,
    PasswordField,
    Field,
    BooleanField,
    ValidationError,
)
from wtforms.widgets import TextInput
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, Optional
from wtforms.fields.html5 import DateField
from datetime import date
from ..models import User
from flask_login import current_user


class CustomField(Field):
    widget = TextInput()

    def _value(self):
        if self.data:
            return "#" + " #".join(self.data)
        else:
            return ""

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [x.strip() for x in valuelist[0].split("#")]
        else:
            self.data = []


class PostTweet(FlaskForm):
    tweet_text = TextAreaField(
        "What you thinking?", validators=[DataRequired(), Length(1, 280)]
    )
    hashtags = CustomField()
    schedule_time = DateField("Schedule Date", validators=[Optional()])
    submit = SubmitField("Post")

    def validate_schedule_time(form, field):
        if field.data is not None and field.data < date.today():
            raise ValidationError("Date must be in the future")


class EditTweetForm(FlaskForm):
    tweet_text = TextAreaField(
        "What you thinking?", validators=[DataRequired(), Length(1, 280)]
    )
    hashtags = CustomField()
    edit = SubmitField("Edit")
    delete = SubmitField("Delete")


class CommentForm(FlaskForm):
    body = StringField("", validators=[DataRequired()])
    submit = SubmitField("Comment")


class EditCommentForm(FlaskForm):
    body = StringField("", validators=[DataRequired()])
    edit = SubmitField("Edit")
    delete = SubmitField("Delete")


class EditProfileForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(1, 64),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Usernames must have only letters, numbers, dots or " "underscores",
            ),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            EqualTo("password2", message="Passwords must mtach!"),
        ],
    )
    password2 = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Update")

    def validate_email(self, field):
        if (
            User.query.filter_by(email=field.data).first()
            and field.data != current_user.email
        ):
            raise ValidationError("Email already registered.")

    def validate_username(self, field):
        if (
            User.query.filter_by(username=field.data).first()
            and field.data != current_user.username
        ):
            raise ValidationError("Username already in use.")
