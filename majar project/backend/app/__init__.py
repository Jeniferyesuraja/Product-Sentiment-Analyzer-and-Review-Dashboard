"""Flask application factory for the Product Sentiment Analyzer."""

from flask import Flask
from flask_cors import CORS

from app.config import Config
from app.database import init_database
from app.routes import api


def create_app(config_class=Config):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    init_database(app.config)

    CORS(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})
    app.register_blueprint(api, url_prefix="/api")

    return app
