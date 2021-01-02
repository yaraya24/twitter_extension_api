from flask import request, jsonify
from . import api
from .. import db
from .schemas import user_schema, tweet_schema, hashtag_schema, comment_schema, scheduled_tweet_schema, users_schema, tweets_schema
from ..models import User, Tweet, Comment, ScheduledTweet
from flask_jwt_extended import jwt_required, get_jwt_identity
from .errors import unauthorized, invalid_request
from datetime import datetime

@api.route('/tweets/all')
def get_all_tweets():    
    tweets = Tweet.query.filter(Tweet.scheduled == None).all()
    return jsonify(tweets_schema.dump(tweets))

@api.route('/tweets/<int:id>')
def get_tweet(id):
    tweets = Tweet.query.get_or_404(id)
    return jsonify(tweet_schema.dump(tweets))

@api.route('/users/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user_schema.dump(user))

@api.route('/users/all')
def get_all_users():
    users = User.query.all()
    return jsonify(users_schema.dump(users))

@api.route('/comments/all')
def get_all_comments():
    comments = Comment.query.all()
    return jsonify(comment_schema.dump(comments))

@api.route("/post_tweet", methods=["POST"])
@jwt_required
def post_tweet():
    tweet_text = request.json.get('text')
    schedule_time = request.json.get('schedule_time')
    if tweet_text is None or tweet_text == '':
        return invalid_request("Text required for new tweet")
    author = User.query.filter_by(username=get_jwt_identity()).first_or_404()
    tweet = Tweet(text=tweet_text, author=author, source='api')
    db.session.add(tweet)
    if schedule_time is not None:
        try:
            datetime.strptime(schedule_time, "%Y-%m-%d")
        except:
            return invalid_request("Schedule date needs to be in YYYY-MM-DD format")
        scheduled_tweet = ScheduledTweet(scheduled_time=schedule_time, tweet=tweet)
        db.session.add(scheduled_tweet)
    db.session.commit()
    return jsonify(tweet_schema.dump(tweet))



@api.route("/delete_tweet/<int:id>", methods=["DELETE"])
@jwt_required
def delete_tweet(id):
    author = User.query.filter_by(username=get_jwt_identity()).first_or_404()
    tweet = Tweet.query.get_or_404(id)
    if tweet.author is not author:
        return unauthorized("You are not authorized")
    db.session.delete(tweet)
    db.session.commit()
    return jsonify(tweet_schema.dump(tweet))

@api.route('/all_data', methods=['GET'])
def all_data():
    all_data = {}

    all_users = db.session.execute('SELECT * FROM users')
    all_data['Users'] = []
    for r in all_users:
        all_data['Users'].append(dict(r))

    all_tweets = db.session.execute('SELECT * FROM tweets')
    all_data['Tweets'] = []
    for r in all_tweets:
        all_data['Tweets'].append(dict(r))

    all_comments = db.session.execute('SELECT * FROM comments')
    all_data['Comments'] = []
    for r in all_comments:
        all_data['Comments'].append(dict(r))
    
    all_scheduled_tweets = db.session.execute('SELECT * FROM scheduled_tweets')
    all_data['Scheduled_Tweets'] = []
    for r in all_scheduled_tweets:
        all_data['Scheduled_Tweets'].append(dict(r))

    all_hashtags = db.session.execute('SELECT * FROM hashtags')
    all_data['Hashtags'] = []
    for r in all_hashtags:
        all_data['Hashtags'].append(dict(r))
    return jsonify(all_data)

    all_follows = db.session.execute('SELECT * FROM follows')
    all_data['Follows'] = []
    for r in all_follows:
        all_data['Follows'].append(dict(r))
    return jsonify(all_data)

@api.route('/statistics', methods=["GET"])
def statistics():
    statistics = {}
    tweet_count = db.session.execute('SELECT COUNT(*) FROM tweets')
    for r in tweet_count:
        statistics['Total_Tweet_Count'] = r['count']
    tweets_by_source_result = db.session.execute('SELECT COUNT(*), source FROM tweets GROUP BY source')
    statistics['Tweets_by_source'] = []
    for r in tweets_by_source_result:
        statistics['Tweets_by_source'].append(dict(r))
    most_followed = db.session.execute("""SELECT t1.username, t2.count as number_of_followers
                                        FROM users as t1
                                        INNER JOIN (
                                            SELECT followed_id, count(*)
                                            FROM follows
                                            GROUP BY followed_id)
                                        AS t2 ON t1.id = t2.followed_id
                                        ORDER BY number_of_followers DESC
                                        LIMIT 1""")
    for r in most_followed:
        statistics['Most_Followed_User'] = dict(r)

    most_active_user = db.session.execute(""" SELECT t1.username, t2.count + t3.count AS total_contributions
                                            FROM users as t1
                                            INNER JOIN (
                                                SELECT author_id, count(*)
                                                FROM tweets
                                                GROUP BY author_id)
                                            AS t2 ON t1.id = t2.author_id
                                            INNER JOIN (
                                                SELECT author_id, COUNT(*)
                                                FROM comments
                                                GROUP BY author_id
                                            )
                                            AS t3 ON t3.author_id = t1.id  
                                            ORDER BY total_contributions DESC
                                            LIMIT 1              
                                            """)
    for r in most_active_user:
        statistics['Most_Active_User'] = dict(r)
    return jsonify(statistics)

