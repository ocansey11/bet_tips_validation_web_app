import os
from app.scraping import user,password,host,dbname,port

class Config:
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{user}:{password}@{host}/{dbname}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'max_overflow': 20,
        'pool_timeout': 30,
        'pool_recycle': 1800
    }

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@localhost/dev_db'

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://test_user:password@localhost/test_db'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
