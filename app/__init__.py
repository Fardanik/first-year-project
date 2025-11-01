from flask import Flask
from .config import Config
from flask_mysqldb import MySQL
import sqlalchemy
from app.database.main import create_database
import datetime

def create_app():
    app = Flask(__name__)  # Initialise Flask app
    app.config.from_object(Config)  # Load config
    app.jinja_env.filters['format_time'] = format_time
    app.jinja_env.filters['format_date'] = format_date

    # database setup
    create_database()

    # Add the routes
    from .routes import main
    app.register_blueprint(main)

    return app

def format_time(timestamp):
    """Format a timestamp into a human-readable time."""
    if timestamp:
        return datetime.fromtimestamp(timestamp).strftime('%I:%M %p')  # Example: 02:30 PM
    return ''

def format_date(timestamp):
    """Format a timestamp into a human-readable date."""
    if timestamp:
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')  # Example: 2023-10-30
    return ''

