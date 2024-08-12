import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://test_user:password@localhost/bet_model_testing'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@localhost/dev_db'

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
