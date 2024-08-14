# app/__init__.py
from flask import Flask # type: ignore
from app.config import Config
from app.utils import db, migrate
from app.routes import admin_bp
from app.routes import standings_bp
from app.routes import matches_bp

def create_app(class_config = Config):
    app = Flask(__name__)
    app.config.from_object(class_config)
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    app.register_blueprint(admin_bp)
    app.register_blueprint(standings_bp)
    app.register_blueprint(matches_bp)


    return app
