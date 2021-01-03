from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_moment import Moment
from flask_marshmallow import Marshmallow
from config import config

db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
moment = Moment()
jwt = JWTManager()
marsh = Marshmallow()
login_manager.login_view = "auth.login"


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    jwt.init_app(app)
    marsh.init_app(app)

    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    from .commands import db_commands

    app.register_blueprint(db_commands)

    from .auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    from .api import api as api_blueprint

    app.register_blueprint(api_blueprint, url_prefix="/api")

    return app
