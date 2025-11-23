from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('app.config.Config')

    db.init_app(app)

    with app.app_context():
        from .routes import blueprint  # Import blueprint
        app.register_blueprint(blueprint)

        # Create database tables for our models
        db.create_all()

        return app

# For gunicorn deployment
app = create_app()