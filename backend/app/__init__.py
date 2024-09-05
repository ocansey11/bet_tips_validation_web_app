# app/__init__.py
from flask import Flask,g # type: ignore
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import Config
from app.utils import db, migrate
from app.routes import admin_bp
from app.routes import standings_bp
from app.routes import matches_bp
from app.routes import training_bp
from app.routes import tables_bp


def create_app(class_config = Config):
    app = Flask(__name__)
    app.config.from_object(class_config)
    db.init_app(app)
    migrate.init_app(app, db)

    # Set up the SQLAlchemy engine and session factory
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], **app.config['SQLALCHEMY_ENGINE_OPTIONS'])
    Session = sessionmaker(bind=engine)

    @app.before_request
    def create_session():
        g.session = Session()

    @app.teardown_request
    def remove_session(exception=None):
        session = g.pop('session', None)
        if session:
            session.close()



    # Register Blueprintsa
    app.register_blueprint(admin_bp)
    app.register_blueprint(standings_bp)
    app.register_blueprint(matches_bp)
    app.register_blueprint(training_bp)
    app.register_blueprint(tables_bp)
 
    return app
