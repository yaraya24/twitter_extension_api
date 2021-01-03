import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """ Important configuration variables that are set 
    in the .env file"""

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY") or "Change this in .env"
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or "Change this in .env"
    ENVIRONMENT = os.environ.get("FLASK_ENV")


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_URI_DEVELOPMENT")


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_URI_TESTING")


class ProductionConfig(Config):

    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_URI_PRODUCTION")


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}
