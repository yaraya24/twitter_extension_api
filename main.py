from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>hellow world!</h1>'

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://yaraya24:yaraya24@localhost:5432/twitter_api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    created_at = db.Column(db.Date, default=datetime.now())


    tweets = db.relationship('Tweet', backref='user', lazy='dynamic') #dynamic ensures the query isn't executed immediately so we can do shit like get it ordered alphabetically

    def __repr__(self):
        return f'<User {self.username}>'


class Tweet(db.Model):
    __tablename__ = 'tweets'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))