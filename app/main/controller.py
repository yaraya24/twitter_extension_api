from flask import render_template, session, redirect, url_for, current_app, flash, request
from .forms import PostTweet, CommentForm, EditProfileForm, EditCommentForm, EditTweetForm
from flask_login import login_required, current_user
from .. import db
from .. models import User, Tweet, Retweet, Comment, Hashtag, ScheduledTweet
from . import main
from datetime import datetime, date


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostTweet()
    if form.validate_on_submit():
        tweet = Tweet(text=form.tweet_text.data, author=current_user._get_current_object())
        db.session.add(tweet)
        for tags in form.hashtags.data:
            if len(tags.strip()) > 0:
                hashtag = Hashtag(name=tags, tweet=tweet)
                db.session.add(hashtag) 
        if form.schedule_time.data:
            scheduled_tweet = ScheduledTweet(scheduled_time=form.schedule_time.data, tweet=tweet)
            db.session.add(scheduled_tweet)
        db.session.commit()
        return redirect(url_for('main.index'))  
    tweets = Tweet.query.filter(Tweet.scheduled == None).all()
    return render_template('index.html', form=form, tweets=tweets, current_time=datetime.utcnow())


# @main.route('/retweet/<int:tweet_id>', methods=['GET', 'POST'])
# @login_required
# def retweet(tweet_id):
#     form = PostTweet()
#     original_tweet = Tweet.query.get_or_404(tweet_id)
#     if form.validate_on_submit():
#         retweet = Retweet(author=current_user._get_current_object(), original=original_tweet, text=form.tweet_text.data)
#         db.session.add(retweet)
#         db.session.commit()
#         flash('Successfully Retweeted')
#         return redirect(url_for('main.index'))
#     form.tweet_text.data = 'Add a comment'
#     return render_template('retweet.html', form=form, original_tweet=original_tweet)


@main.route('/tweet/<int:tweet_id>', methods=['GET', 'POST'])

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
    hashtags = tweet.hashtags
    return render_template('tweets.html', tweet=tweet, form=form, comments=comments, hashtags=hashtags)

@main.route('/tweet/<int:tweet_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_tweet(tweet_id):  
    tweet = Tweet.query.get_or_404(tweet_id)
    if current_user != tweet.author:
        return render_template('404.html'), 404
    form = EditTweetForm()
    if form.validate_on_submit(): 
        if form.delete.data:
            db.session.delete(tweet)
            db.session.commit()
            return redirect(url_for('main.index'))
        tweet.text = form.tweet_text.data
        tweet.created_at = datetime.utcnow()
        db.session.add(tweet)
        [db.session.delete(tags) for tags in tweet.hashtags]
        for tags in form.hashtags.data:
            if len(tags.strip()) > 0:
                hashtag = Hashtag(name=tags, tweet=tweet)
                db.session.add(hashtag)
        db.session.commit()
        flash('Succesfully Updated')
        return redirect(url_for('main.tweet', tweet_id=tweet.id))
    form.tweet_text.data = tweet.text
    list_of_hashtags = [x.name for x in tweet.hashtags]
    form.hashtags.data = list_of_hashtags
    return render_template('edit_tweets.html', form=form)




@main.route('/user/<username>', methods=['GET', 'POST'])
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    # user_tweets = user.tweets.filter(Tweet.scheduled!=None).all()
    # user_tweets = Tweet.query.filter(Tweet.scheduled == None).filter_by(author=username)
    user_tweets = Tweet.query.filter_by(author=user).filter(Tweet.scheduled==None).all()
    scheeduled_tweets = Tweet.query.filter_by(author=user).filter(Tweet.scheduled!=None).all()
    
    return render_template('user.html', user=user, user_tweets=user_tweets, scheduled_tweets=scheeduled_tweets)

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


@main.route('/comment/<int:comment_id>', methods=['GET', 'POST'])
def edit_comment(comment_id):
    form = EditCommentForm()
    comment = Comment.query.get_or_404(comment_id)
    tweet_id = comment.tweet.id
    if form.validate_on_submit():
        if form.delete.data:
            db.session.delete(comment)
            db.session.commit()
            return redirect(url_for('main.tweet', tweet_id=tweet_id))
        comment.body = form.body.data
        comment.created_at = datetime.utcnow()
        db.session.add(comment)
        db.session.commit()
        flash("Successfully Updated")
        return redirect(url_for('main.tweet', tweet_id=comment.tweet.id))
    form.body.data = comment.body
    return render_template('comments.html', form=form)


@main.route('/follow/<username>', methods=['GET', 'POST'])
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return redirect(url_for('main.index'))
    if current_user.is_following(user):
        current_user.unfollow(user)
        db.session.commit()
        flash(f"You are no longer following {user.username}")
        return redirect(url_for('.user', username=username))    
    current_user.follow(user)
    db.session.commit()
    flash(f"You are now following {user.username}")
    return redirect(url_for('.user', username=username))