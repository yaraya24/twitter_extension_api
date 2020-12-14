import os

class Config:

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_APP = 'main.py'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://yaraya24:yaraya24@localhost:5432/twitter_api'

class TestingConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://yaraya24:yaraya24@localhost:5432/twitter_api'

class ProductionConfig(Config):
    
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://yaraya24:yaraya24@localhost:5432/twitter_api'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}