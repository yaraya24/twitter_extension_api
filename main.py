import os
from flask_migrate import Migrate
from app import create_app, db
from app.models import User, Tweet, ScheduledTweet


app = create_app(os.getenv("FLASK_ENV") or "default")
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    """ Function that passes important classes to the flask shell """
    return dict(
        db=db, User=User, Tweet=Tweet, ScheduledTweet=ScheduledTweet
    )
