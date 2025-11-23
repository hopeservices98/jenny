import os

class Config:
    """Set Flask configuration from environment variables."""

    # General Config
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    FLASK_APP = os.environ.get('FLASK_APP') or 'run.py'
    FLASK_ENV = os.environ.get('FLASK_ENV') or 'development'

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or "sqlite:///../instance/jenny_memory.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # OpenRouter API
    OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')
    OPENROUTER_MODEL = os.environ.get('OPENROUTER_MODEL') or "x-ai/grok-4.1-fast:free"

    # Image Directory
    IMAGE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'images'))