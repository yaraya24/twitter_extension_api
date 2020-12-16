from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo


class PostTweet(FlaskForm):
    tweet_text = TextAreaField("What you thinking?", validators=[DataRequired(), Length(1,280)])
    submit = SubmitField('Post')

class CommentForm(FlaskForm):
    body = StringField('', validators=[DataRequired()])    
    submit = SubmitField('Submit')

class EditCommentForm(FlaskForm):
    body = StringField('', validators=[DataRequired()])    
    edit = SubmitField('Edit')
    delete = SubmitField('Delete')


class EditProfileForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1 ,64), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1 ,64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,'Usernames must have only letters, numbers, dots or ''underscores')])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message={'Passwords must mtach!'})])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Update')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')
