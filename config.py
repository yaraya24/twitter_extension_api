import os


class Config:
    """ Important configuration variables"""

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_APP = "main.py"
    SECRET_KEY = os.environ.get("SECRET_KEY") or "hard to guess string"
    JWT_SECRET_KEY = "duck"


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        "postgresql+psycopg2://yaraya24:yaraya24@localhost:5432/twitter_api"
    )


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False  # Removes CSRF token for testing purposes
    SQLALCHEMY_DATABASE_URI = (
        "postgresql+psycopg2://yaraya24:yaraya24@localhost:5432/twitter_api"
    )


class ProductionConfig(Config):

    SQLALCHEMY_DATABASE_URI = (
        "postgresql+psycopg2://yaraya24:yaraya24@localhost:5432/twitter_api"
    )


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}