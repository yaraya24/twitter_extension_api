from flask import render_template, session, redirect, url_for, current_app, flash, request
from .forms import PostTweet
from flask_login import login_required, current_user
from .. import db
from .. models import User, Tweet
from . import main


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostTweet()
    if form.validate_on_submit():
        tweet = Tweet(text=form.tweet_text.data, author=current_user._get_current_object())
        db.session.add(tweet)
        db.session.commit()
        return redirect(url_for('main.index'))  
    tweets = Tweet.query.order_by(Tweet.created_at.desc())
    return render_template('index.html', form=form, tweets=tweets)