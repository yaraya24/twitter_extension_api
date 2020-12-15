from flask import render_template, session, redirect, url_for, current_app, flash, request
from .forms import PostTweet, CommentForm, EditProfileForm
from flask_login import login_required, current_user
from .. import db
from .. models import User, Tweet, Retweet, Comment
from . import main
from datetime import datetime


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostTweet()
    if form.validate_on_submit():
        tweet = Tweet(text=form.tweet_text.data, author=current_user._get_current_object())
        db.session.add(tweet)
        db.session.commit()
        return redirect(url_for('main.index'))  
    tweets = Tweet.query.order_by(Tweet.created_at.desc())

    return render_template('index.html', form=form, tweets=tweets, current_time=datetime.utcnow())


@main.route('/retweet/<int:tweet_id>', methods=['GET', 'POST'])
@login_required
def retweet(tweet_id):
    form = PostTweet()
    original_tweet = Tweet.query.get_or_404(tweet_id)
    if form.validate_on_submit():
        retweet = Retweet(author=current_user._get_current_object(), original=original_tweet, text=form.tweet_text.data)
        db.session.add(retweet)
        db.session.commit()
        flash('Successfully Retweeted')
        return redirect(url_for('main.index'))
    form.tweet_text.data = 'Add a comment'
    return render_template('retweet.html', form=form, original_tweet=original_tweet)


@main.route('/tweet/<int:tweet_id>', methods=['GET', 'POST'])
@login_required
def tweet(tweet_id):
    tweet = Tweet.query.get_or_404(tweet_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data, tweet=tweet, author=current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()
        flash("Your comment has been added")
        return redirect(url_for('main.tweet', tweet_id=tweet.id))
    comments = tweet.comments.order_by(Comment.created_at.asc())
    return render_template('tweets.html', tweets=tweet, form=form, comments=comments)


@main.route('/user/<username>', methods=['GET', 'POST'])
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.password = form.password.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash("Successfully Updated")
        return redirect(url_for('main.user', username=current_user.username))
    form.username.data = current_user.username
    form.email.data = current_user.email
    return render_template('edit_profile.html', form=form)
